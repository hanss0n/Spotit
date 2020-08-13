<template>

    <div class="parameters">
        <form class="params">


            <label for="num_cluster">Clusters:</label>
            <input type="number" id="num_cluster" value="0" v-model="num_clusters" max="10" min="1">

            <label>Acousticness</label>
            <label class="switch">
                <input type="checkbox" value="acousticness" v-model="selected">
                <span class="slider round"></span>
            </label>

            <label>Danceability</label>
            <label class="switch">
                <input type="checkbox" value="danceability" v-model="selected">
                <span class="slider round"></span>
            </label>

            <label>Energy</label>
            <label class="switch">
                <input type="checkbox" value="energy" v-model="selected">
                <span class="slider round"></span>
            </label>

            <label>Instrumentalness</label>
            <label class="switch">
                <input type="checkbox" value="instrumentalness" v-model="selected">
                <span class="slider round"></span>
            </label>

            <label>Speechiness</label>
            <label class="switch">
                <input type="checkbox" value="speechiness" v-model="selected">
                <span class="slider round"></span>
            </label>



        </form>
        <form class="uri" @submit.prevent="generateCluster">
            <input type="text" v-model="list_uri" name="list_uri" placeholder="Enter Spotify list URL/URI...">
            <input type="submit" value="Clustrify!" class="btn">
        </form>
    </div>

</template>

<script>
    export default {
        name: "GenerateCluster",
        data() {
            return {
                list_uri: '',
                selected: ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'],
                num_clusters: 5
            }

        },
        methods: {
            generateCluster() {
                const regex = '/.*playlist.(.{22}).*/';
                const subst = `spotify:playlist:$1`;
                this.list_uri = this.list_uri.replace(regex, subst);
                console.log(this.list_uri)
                const params = {
                    list_uri: this.list_uri,
                    num_clusters: this.num_clusters,
                    attributes: this.selected
                }
                this.$emit('generate-cluster', params);
            }
        }
    }
</script>

<style scoped>
    form[class="uri"] {
        display: flex;
        background: #292929;
        color: white;
        border-bottom: 1px outset #a3a3a3;
    }

    form[class="params"] {
        display: flex;
        background: #292929;
        color: white;
    }

    input[type="text"] {
        flex: 10;
        border-bottom-left-radius: 20px;
        border-top-left-radius: 20px;

        padding: 6px 14px;
        margin: 4px 0 4px 4px;
        display: inline-block;
        border: 1px solid #ccc;
        box-sizing: border-box;
    }

    input[type="submit"] {
        flex: 2;
        border-bottom-right-radius: 20px;
        border-top-right-radius: 20px;
        background-color: #1db954;
        margin: 4px 4px 4px 0;
    }

    input[type=submit]:hover {
        background-color: #097910;
    }

    .parameters input[type="number"] {
        width: 70px;
        border-radius: 20px;
        padding: 2px 12px;
        margin: 4px 30px 4px 4px;
        display: inline-block;
        border: 1px solid #ccc;
        box-sizing: border-box;
    }

    .parameters label {
        margin: 3px 0 0 8px;
    }

    .switch {
        position: relative;
        display: inline-block;
        width: 47px;
        height: 20px;

    }

    .switch input {
        display: none;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #505050;
        -webkit-transition: .4s;
        transition: .4s;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 13px;
        width: 13px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        -webkit-transition: .4s;
        transition: .4s;
    }

    input:checked + .slider {
        background-color: #1db954;
    }

    input:focus + .slider {
        box-shadow: 0 0 1px #1db954;
    }

    input:checked + .slider:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }

    /* Rounded sliders */
    .slider.round {
        border-radius: 34px;
    }

    .slider.round:before {
        border-radius: 50%;
    }
</style>