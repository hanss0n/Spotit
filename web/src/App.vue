<template>
    <div id="app">
        <Header/>
        <GenerateCluster v-on:generate-cluster="getSongData"/>
        <ClusterGraph v-bind:song_data="song_data" v-bind:num_clusters="num_clusters"/>
    </div>
</template>

<script>
    import axios from 'axios'
    import Header from '@/components/layout/Header';
    import GenerateCluster from "@/components/GenerateCluster";
    import ClusterGraph from "@/components/ClusterGraph";

    export default {
        name: 'App',
        components: {
            ClusterGraph,
            GenerateCluster,
            Header
        },
        data() {
            return {
                num_clusters: 5,
                song_data: []
            }
        },
        methods: {
            getSongData(params) {
                this.num_clusters = params["num_clusters"]
                axios.post('https://clustrify-2arzmeuymq-lz.a.run.app/spotify_list/', params)
                    .then(x => this.song_data = x.data)
                    .catch(e => console.log(e))
            }
        }
    }
</script>

<style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.4;
        background: black;
    }

    .btn {
        display: inline-block;
        border: none;
        background: #555;
        color: #fff;
        padding: 7px 20px;
        cursor: pointer;
    }

    .btn:hover {
        background: #666;
    }
</style>
