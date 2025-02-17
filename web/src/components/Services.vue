<template>
  <div class="q-pa-md">
    <q-table
      dense
      :table-class="{ 'table-bgcolor': !$q.dark.isActive, 'table-bgcolor-dark': $q.dark.isActive }"
      class="remote-bg-tbl-sticky"
      :rows="servicesData"
      :columns="columns"
      v-model:pagination="pagination"
      :filter="filter"
      row-key="display_name"
      binary-state-sort
      hide-bottom
    >
      <template v-slot:top>
        <q-btn dense flat push @click="getServices" icon="refresh" />
        <q-space />
        <q-input v-model="filter" outlined label="Search" dense clearable>
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-menu context-menu>
            <q-list dense style="min-width: 200px">
              <q-item clickable v-close-popup @click="serviceAction(props.row.name, 'start', props.row.display_name)">
                <q-item-section>Start</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="serviceAction(props.row.name, 'stop', props.row.display_name)">
                <q-item-section>Stop</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="serviceAction(props.row.name, 'restart', props.row.display_name)">
                <q-item-section>Restart</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup @click="editService(props.row.name)">
                <q-item-section>Service Details</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <q-td key="display_name" :props="props">
            <q-icon name="fas fa-cogs" />
            &nbsp;&nbsp;&nbsp;{{ props.row.display_name }}
          </q-td>
          <q-td key="start_type" :props="props">{{ props.row.start_type }}</q-td>
          <q-td key="pid" :props="props">{{ props.row.pid }}</q-td>
          <q-td key="status" :props="props">{{ props.row.status }}</q-td>
          <q-td key="username" :props="props">{{ props.row.username }}</q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="serviceDetailsModal">
      <q-card style="width: 600px; max-width: 80vw">
        <q-card-section>
          <div class="text-h6">Service Details - {{ serviceData.display_name }}</div>
        </q-card-section>

        <q-card-section>
          <div class="row">
            <div class="col-3">Service name:</div>
            <div class="col-9">{{ serviceData.svc_name }}</div>
          </div>
          <br />
          <div class="row">
            <div class="col-3">Display name:</div>
            <div class="col-9">{{ serviceData.display_name }}</div>
          </div>
          <br />
          <div class="row">
            <div class="col-3">Description:</div>
            <div class="col-9">
              <q-field outlined :color="$q.dark.isActive ? 'white' : 'black'">{{ serviceData.description }}</q-field>
            </div>
          </div>
          <br />
          <div class="row">
            <div class="col-3">Path:</div>
            <div class="col-9">
              <code>{{ serviceData.binpath }}</code>
            </div>
          </div>
          <br />
          <br />
          <div class="row">
            <div class="col-3">Startup type:</div>
            <div class="col-5">
              <q-select
                @update:model-value="startupTypeChanged"
                dense
                options-dense
                outlined
                v-model="startupType"
                :options="startupOptions"
              />
            </div>
          </div>
        </q-card-section>
        <hr />
        <q-card-section>
          <div class="row">
            <div class="col-3">Service status:</div>
            <div class="col-9">{{ serviceData.status }}</div>
          </div>
          <br />
          <div class="row">
            <q-btn-group push>
              <q-btn
                color="gray"
                glossy
                :text-color="$q.dark.isActive ? 'white' : 'black'"
                push
                label="Start"
                @click="serviceAction(serviceData.svc_name, 'start', serviceData.display_name)"
              />
              <q-btn
                color="gray"
                glossy
                :text-color="$q.dark.isActive ? 'white' : 'black'"
                push
                label="Stop"
                @click="serviceAction(serviceData.svc_name, 'stop', serviceData.display_name)"
              />
              <q-btn
                color="gray"
                glossy
                :text-color="$q.dark.isActive ? 'white' : 'black'"
                push
                label="Restart"
                @click="serviceAction(serviceData.svc_name, 'restart', serviceData.display_name)"
              />
            </q-btn-group>
          </div>
        </q-card-section>
        <hr />
        <q-card-actions align="left" :class="$q.dark.isActive ? 'text-teal' : 'bg-white text-teal'">
          <q-btn
            :disable="saveServiceDetailButton"
            dense
            label="Save"
            color="positive"
            @click="changeStartupType(startupType, serviceData.svc_name)"
          />
          <q-btn dense label="Cancel" color="grey" v-close-popup />
        </q-card-actions>
        <q-inner-loading :showing="serviceDetailVisible" />
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import mixins from "@/mixins/mixins";

export default {
  name: "Services",
  props: ["pk"],
  mixins: [mixins],
  data() {
    return {
      servicesData: [],
      serviceDetailsModal: false,
      serviceDetailVisible: false,
      saveServiceDetailButton: true,
      serviceData: {},
      startupType: "",
      startupOptions: ["Automatic (Delayed Start)", "Automatic", "Manual", "Disabled"],
      filter: "",
      pagination: {
        rowsPerPage: 9999,
        sortBy: "display_name",
        descending: false,
      },
      columns: [
        {
          name: "display_name",
          label: "Name",
          field: "display_name",
          align: "left",
          sortable: true,
        },
        {
          name: "start_type",
          label: "Startup",
          field: "start_type",
          align: "left",
          sortable: true,
        },
        {
          name: "pid",
          label: "PID",
          field: "pid",
          align: "left",
          sortable: true,
        },
        {
          name: "status",
          label: "Status",
          field: "status",
          align: "left",
          sortable: true,
        },
        {
          name: "username",
          label: "Log On As",
          field: "username",
          align: "left",
          sortable: true,
        },
      ],
    };
  },
  methods: {
    changeStartupType(startuptype, name) {
      let changed;
      switch (startuptype) {
        case "Automatic (Delayed Start)":
          changed = "autodelay";
          break;
        case "Automatic":
          changed = "auto";
          break;
        case "Manual":
          changed = "manual";
          break;
        case "Disabled":
          changed = "disabled";
          break;
        default:
          changed = "nothing";
      }
      const data = {
        pk: this.pk,
        sv_name: name,
        edit_action: changed,
      };
      this.serviceDetailVisible = true;
      this.$axios
        .post("/services/editservice/", data)
        .then(r => {
          this.serviceDetailVisible = false;
          this.serviceDetailsModal = false;
          this.getServices();
          this.notifySuccess(`Service ${name} was edited!`);
        })
        .catch(e => {
          this.serviceDetailVisible = false;
        });
    },
    startupTypeChanged() {
      this.saveServiceDetailButton = false;
    },
    editService(name) {
      this.saveServiceDetailButton = true;
      this.serviceDetailsModal = true;
      this.serviceDetailVisible = true;
      this.$axios
        .get(`/services/${this.pk}/${name}/servicedetail/`)
        .then(r => {
          this.serviceData = r.data;
          this.serviceData.svc_name = name;
          this.startupType = this.serviceData.start_type;
          if (this.serviceData.start_type === "Automatic" && this.serviceData.autodelay === true) {
            this.startupType = "Automatic (Delayed Start)";
          } else if (this.serviceData.start_type === "Automatic" && this.serviceData.autodelay === false) {
            this.startupType = "Automatic";
          }
          this.serviceDetailVisible = false;
        })
        .catch(e => {
          this.serviceDetailVisible = false;
          this.serviceDetailsModal = false;
        });
    },
    serviceAction(name, action, fullname) {
      let msg, status;
      switch (action) {
        case "start":
          msg = "Starting";
          status = "started";
          break;
        case "stop":
          msg = "Stopping";
          status = "stopped";
          break;
        case "restart":
          msg = "Restarting";
          status = "restarted";
          break;
        default:
          msg = "error";
      }
      this.$q.loading.show({ message: `${msg} service ${fullname}` });
      const data = {
        pk: this.pk,
        sv_name: name,
        sv_action: action,
      };
      this.$axios
        .post("/services/serviceaction/", data)
        .then(r => {
          this.getServices();
          this.serviceDetailsModal = false;
          this.notifySuccess(`Service ${fullname} was ${status}!`);
        })
        .catch(e => {
          this.$q.loading.hide();
        });
    },
    getServices() {
      this.$q.loading.show({ message: "Loading services..." });
      this.$axios
        .get(`/services/${this.pk}/services/`)
        .then(r => {
          this.servicesData = [r.data][0].services;
          this.$q.loading.hide();
        })
        .catch(e => {
          this.$q.loading.hide();
        });
    },
  },
  mounted() {
    this.getServices();
  },
};
</script>