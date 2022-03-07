<template>
  <div id="app">
    <b-modal ref="modalPopover" id="modalPopover" title="Alert" ok-only>
      <p>
        {{ errorMessage }}
      </p>
    </b-modal>
    <div class="container">
      <div class="row">
        <h1 class="text-left">Info about this computer</h1>
      </div>
      <div class="row">
        <hr class="mt-2 mb-3"/>
      </div>
    </div>
    <div class="container hscroll">
      <b-table
        ref="processTable"
        sticky-header
        striped
        hover
        fixed=true
        selectable=true
        select-mode="single"
        :items="processes"
        :fields="fields_processes"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :label-sort-asc="empty"
        :label-sort-clear="empty"
        :label-sort-desc="empty"
        @row-selected="onRowSelected"
      >
      </b-table>
    </div>
  </div>
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'
import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
//import axios from 'axios'
//import date from 'date-and-time';
//import VueAxios from 'vue-axios'
import VueEllipseProgress from 'vue-ellipse-progress';


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './css/style.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
//Vue.use(VueAxios, axios)
Vue.use(VueEllipseProgress);


export default {
  name: 'App',
  components: {
  },
  data() {
    return {
      selectedPid: -1,
      empty: '',
      sortBy: 'cpu_percent',
      sortDesc: true,
      processes: [],
      fields_processes: ['pid', 'name', {'key': 'cpu_percent', sortable: true, sortDirection: 'last'},
        'create_time', 'exe', {'key': 'memory_percent', sortable: true, sortDirection: 'last'},
        'nice', 'status', {'key': 'username', sortable: true, sortDirection: 'last'}],
      cpu_percentage: 0,
      mem_percentage: 0,
      swap_percentage: 0,
    }
  },
  mounted() {
    window.addEventListener("keypress", e => {
      this.keyPressed(String.fromCharCode(e.keyCode));
    });

    let connection = new WebSocket('ws://localhost:3000');
    connection.onmessage = (event) => {
      console.log("I'm on connection.onmessage")
      let response = JSON.parse(event.data);
      switch(response.command) {
        case "ping":
          this.processes = response.data.processes;
          if (this.selectedPid > -1) {
            let i = 0;
            for (const line of this.processes) {
              if (line.pid == this.selectedPid)
                this.$refs.processTable.selectRow(i);
              i+=1;
            }
          }
          break;
        case "kill":
          if (response.status == "error")
            console.log("DEU XABUUUUU!!!!!");
          else
            console.log("APARENTEMENTE TÁ TUDO BEM!!!!!");
          break;
      }
    }
    connection.addEventListener('message', function (event) {
      console.log(event == null);
      console.log("I'm on connection.addEventListener");
    });

    let intervalId = setInterval(function(){
      connection.send(JSON.stringify(
        {'command': 'ping', data: {}}
      ));
    }, 10000);
    console.log(intervalId);

  },
  methods: {
    sendKillProcess(){
      // check if there's a line selected
      if (this.selectedPid > -1) {
        // if yes, get pid and send
        this.connection.send(JSON.stringify(
          {'command': 'kill', data: {'pid': this.selectedPid}}
        ));
      }
    },
    keyPressed(key){
      switch(key){
        case 'k':
          this.sendKillProcess();
          break;
      }
    },
    onRowSelected(items){
      console.log("blablabla");
      console.log(items[0]);
      this.selectedPid = items[0].pid;
    },
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
