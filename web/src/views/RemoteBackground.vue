<template>
  <div class="q-pa-md">
    <q-tabs
      v-model="tab"
      dense
      inline-label
      class="text-grey"
      active-color="primary"
      indicator-color="primary"
      align="left"
      narrow-indicator
    >
      <q-tab name="terminal" icon="fas fa-terminal" label="Terminal" />
      <q-tab name="filebrowser" icon="far fa-folder-open" label="File Browser" />
      <q-tab name="services" icon="fas fa-cogs" label="Services" />
      <q-tab name="processes" icon="fas fa-chart-area" label="Processes" />
      <q-tab name="eventlog" icon="fas fa-clipboard-list" label="Event Log" />
    </q-tabs>
    <q-separator />
    <q-tab-panels v-model="tab">
      <q-tab-panel name="terminal">
        <iframe
          style="overflow: hidden; height: 715px"
          :src="terminal"
          width="100%"
          height="100%"
          scrolling="no"
        ></iframe>
      </q-tab-panel>
      <q-tab-panel name="processes">
        <ProcessManager :pk="pk" />
      </q-tab-panel>
      <q-tab-panel name="services">
        <Services :pk="pk" />
      </q-tab-panel>
      <q-tab-panel name="eventlog">
        <EventLog :pk="pk" />
      </q-tab-panel>
      <q-tab-panel name="filebrowser">
        <iframe style="overflow: hidden; height: 715px" :src="file" width="100%" height="100%" scrolling="no"></iframe>
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script>
import ProcessManager from "@/components/ProcessManager";
import Services from "@/components/Services";
import EventLog from "@/components/EventLog";

import { createMetaMixin } from "quasar";

export default {
  name: "RemoteBackground",
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.title,
      };
    }),
  ],
  components: {
    Services,
    EventLog,
    ProcessManager,
  },
  data() {
    return {
      terminal: "",
      file: "",
      tab: "terminal",
      title: "",
      darkMode: true,
    };
  },
  methods: {
    genURLS() {
      this.$axios
        .get(`/agents/${this.pk}/meshcentral/`)
        .then(r => {
          this.terminal = r.data.terminal;
          this.file = r.data.file;
          this.title = `${r.data.hostname} - ${r.data.client} - ${r.data.site} | Remote Background`;
        })
        .catch(e => {});
    },
    getUI() {
      this.$store.dispatch("getDashInfo").then(r => {
        this.darkMode = r.data.dark_mode;
        this.$q.dark.set(this.darkMode);
        this.$q.loadingBar.setDefaults({ color: r.data.loading_bar_color });
      });
    },
  },
  computed: {
    pk() {
      return this.$route.params.pk;
    },
  },
  mounted() {
    this.getUI();
    this.genURLS();
  },
};
</script>