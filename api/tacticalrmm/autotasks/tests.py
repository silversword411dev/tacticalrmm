from unittest.mock import patch
from model_bakery import baker, seq
from itertools import cycle
from autotasks.models import AutomatedTask

from tacticalrmm.test import TacticalTestCase

from .serializers import AutoTaskSerializer


class TestAutotaskViews(TacticalTestCase):
    def setUp(self):
        self.authenticate()
        self.setup_coresettings()

    @patch("automation.tasks.generate_agent_tasks_from_policies_task.delay")
    @patch("autotasks.tasks.create_win_task_schedule.delay")
    def test_add_autotask(
        self, create_win_task_schedule, generate_agent_tasks_from_policies_task
    ):
        url = "/tasks/automatedtasks/"

        # setup data
        script = baker.make_recipe("scripts.script")
        agent = baker.make_recipe("agents.agent")
        agent_old = baker.make_recipe("agents.agent", version="0.9.0")
        policy = baker.make("automation.Policy")
        check = baker.make_recipe("checks.diskspace_check", agent=agent)

        # test script set to invalid pk
        data = {"autotask": {"script": 500}}

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 404)

        # test invalid policy
        data = {"autotask": {"script": script.id}, "policy": 500}

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 404)

        # test invalid agent
        data = {
            "autotask": {"script": script.id},
            "agent": 500,
        }

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 404)

        # test invalid agent version
        data = {
            "autotask": {"script": script.id, "script_args": ["args"]},
            "agent": agent_old.id,
        }

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 400)

        # test add task to agent
        data = {
            "autotask": {
                "name": "Test Task Scheduled with Assigned Check",
                "run_time_days": [0, 1, 2],
                "run_time_minute": "10:00",
                "timeout": 120,
                "enabled": True,
                "script": script.id,
                "script_args": None,
                "task_type": "scheduled",
                "assigned_check": check.id,
            },
            "agent": agent.id,
        }

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 200)

        create_win_task_schedule.assert_called()

        # test add task to policy
        data = {
            "autotask": {
                "name": "Test Task Manual",
                "timeout": 120,
                "enabled": True,
                "script": script.id,
                "script_args": None,
                "task_type": "manual",
                "assigned_check": None,
            },
            "policy": policy.id,
        }

        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 200)

        generate_agent_tasks_from_policies_task.assert_called_with(policy.id)

        self.check_not_authenticated("post", url)

    def test_get_autotask(self):

        # setup data
        agent = baker.make_recipe("agents.agent")
        baker.make("autotasks.AutomatedTask", agent=agent, _quantity=3)

        url = f"/tasks/{agent.id}/automatedtasks/"

        resp = self.client.get(url, format="json")
        serializer = AutoTaskSerializer(agent)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, serializer.data)

        self.check_not_authenticated("get", url)

    @patch("autotasks.tasks.enable_or_disable_win_task.delay")
    @patch("automation.tasks.update_policy_task_fields_task.delay")
    def test_update_autotask(
        self, update_policy_task_fields_task, enable_or_disable_win_task
    ):
        # setup data
        agent = baker.make_recipe("agents.agent")
        agent_task = baker.make("autotasks.AutomatedTask", agent=agent)
        policy = baker.make("automation.Policy")
        policy_task = baker.make("autotasks.AutomatedTask", policy=policy)

        # test invalid url
        resp = self.client.patch("/tasks/500/automatedtasks/", format="json")
        self.assertEqual(resp.status_code, 404)

        url = f"/tasks/{agent_task.id}/automatedtasks/"

        # test editing agent task
        data = {"enableordisable": False}

        resp = self.client.patch(url, data, format="json")
        self.assertEqual(resp.status_code, 200)
        enable_or_disable_win_task.assert_called_with(pk=agent_task.id, action=False)

        url = f"/tasks/{policy_task.id}/automatedtasks/"

        # test editing policy task
        data = {"enableordisable": True}

        resp = self.client.patch(url, data, format="json")
        self.assertEqual(resp.status_code, 200)
        update_policy_task_fields_task.assert_called_with(policy_task.id, True)

        self.check_not_authenticated("patch", url)

    @patch("autotasks.tasks.delete_win_task_schedule.delay")
    @patch("automation.tasks.delete_policy_autotask_task.delay")
    def test_delete_autotask(
        self, delete_policy_autotask_task, delete_win_task_schedule
    ):
        # setup data
        agent = baker.make_recipe("agents.agent")
        agent_task = baker.make("autotasks.AutomatedTask", agent=agent)
        policy = baker.make("automation.Policy")
        policy_task = baker.make("autotasks.AutomatedTask", policy=policy)

        # test invalid url
        resp = self.client.delete("/tasks/500/automatedtasks/", format="json")
        self.assertEqual(resp.status_code, 404)

        # test delete agent task
        url = f"/tasks/{agent_task.id}/automatedtasks/"
        resp = self.client.delete(url, format="json")
        self.assertEqual(resp.status_code, 200)
        delete_win_task_schedule.assert_called_with(pk=agent_task.id)

        # test delete policy task
        url = f"/tasks/{policy_task.id}/automatedtasks/"
        resp = self.client.delete(url, format="json")
        self.assertEqual(resp.status_code, 200)
        delete_policy_autotask_task.assert_called_with(policy_task.id)

        self.check_not_authenticated("delete", url)

    @patch("autotasks.tasks.run_win_task.delay")
    def test_run_autotask(self, run_win_task):
        # setup data
        agent = baker.make_recipe("agents.agent")
        task = baker.make("autotasks.AutomatedTask", agent=agent)

        # test invalid url
        resp = self.client.get("/tasks/runwintask/500/", format="json")
        self.assertEqual(resp.status_code, 404)

        # test run agent task
        url = f"/tasks/runwintask/{task.id}/"
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, 200)
        run_win_task.assert_called_with(task.id)

        self.check_not_authenticated("get", url)
