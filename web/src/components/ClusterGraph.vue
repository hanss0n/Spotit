<template>

    <div class="cluster-graph" ref="chartdiv" v-bind:song_data="song_data" v-bind:num_clusters="num_clusters">
    </div>

</template>

<script>
    import * as am4core from "@amcharts/amcharts4/core";
    import * as am4plugins_forceDirected from "@amcharts/amcharts4/plugins/forceDirected";
    import * as am4plugins_bullets from "@amcharts/amcharts4/plugins/bullets";

    export default {
        name: "ClusterGraph",
        props: ["song_data", "num_clusters"],
        watch: {
            //TODO: the song data must be parsed into a json list with clusters that have children
            // Which are songs. See series_data variable for info.
            // Maybe also pass a num_clusters variable for this?
            song_data: function () {
                let cluster_data = []
                let num_clusters = this.num_clusters
                console.log(num_clusters)
                for (let i = 0; i < num_clusters; i++) {
                    cluster_data.push(
                        {
                            "cluster_num": i + 1,
                            "id": i,
                            "type": "cluster",
                            "children": []
                        }
                    )
                }
                for (let i = 0; i < this.song_data.length; i++) {
                    let track = this.song_data[i]
                    track["type"] = "node"
                    let cluster_id = track["cluster_id"]
                    cluster_data[cluster_id].children.push(track)
                    console.log(cluster_data[cluster_id])
                }
                console.log("Cluster data: ", cluster_data)
                this.chart.data = cluster_data
            }
        },
        methods: {
            playSound(preview_url) {
                if (preview_url) {
                    console.log("Playing ", preview_url)
                    let audio = new Audio(preview_url)
                    audio.volume = 0.02
                    audio.play()

                    return audio
                }
                return null
            },
            stopSound(audio) {
                if (audio) {
                    audio.pause()
                }
            },
            initGraph() {
                // Create chart
                this.chart = am4core.create("cluster-graph", am4plugins_forceDirected.ForceDirectedTree);
                // Create series
                let series = this.chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

                let audio = null

                series.nodes.template.adapter.add("tooltipText", function (text, target) {
                    if (target.dataItem) {
                        switch (target.dataItem.level) {
                            case 0:
                                return target.dataItem.dataContext.children.length +
                                    " track" + (target.dataItem.dataContext.children.length !== 1 ? "s" : "")
                                    + " (Click to toggle)";
                            case 1: {
                                // Build the Normal track tooltip consisting of the track name and artists performing it
                                let toolTipText = target.dataItem.dataContext["name"] + " - "
                                let num_artists = target.dataItem.dataContext.artists.length
                                for (let i = 0; i < num_artists; i++) {
                                    let artist = target.dataItem.dataContext.artists[i]["name"]
                                    toolTipText = toolTipText.concat(artist)
                                    if (i === num_artists - 2 && num_artists > 1) {
                                        toolTipText = toolTipText.concat(" and ")
                                    } else if (i < num_artists - 1) {
                                        toolTipText = toolTipText.concat(", ")
                                    }
                                }

                                // If the track lacks a preview, notify the user and redirect to Spotify
                                if (target.dataItem.dataContext["preview_url"] === null) {
                                    toolTipText = toolTipText.concat("\n (No preview available, click " +
                                        "here to open Spotify web player)")
                                }
                                return toolTipText;
                            }
                        }
                    }
                    return text;
                });

                series.nodes.template.events.on("over", function (ev) {
                    let type = ev.target.dataItem.dataContext.type
                    if (type === "node") {
                        let preview_url = ev.target.dataItem.dataContext["preview_url"]
                        if (preview_url !== "") {
                            audio = this.playSound(preview_url)
                        }
                    }
                }, this);

                series.nodes.template.events.on("out", function (ev) {
                    let type = ev.target.dataItem.dataContext.type
                    if (type === "node") {
                        this.stopSound(audio)
                    }
                }, this)

                series.nodes.template.events.on("hit", function (ev) {
                    let spotify_link = ev.target.dataItem.dataContext.external_urls["spotify"]
                    if (spotify_link !== null) {
                        window.open(spotify_link)
                    }
                }, this)

                //fix cluster type node colors
                series.nodes.template.outerCircle.fill = am4core.color("#000")

                //tooltip shadow styling
                let shadow = series.tooltip.background.filters.getIndex(0);
                shadow.dx = 5;
                shadow.dy = 5;
                shadow.blur = 10;
                shadow.color = am4core.color("#fff");
                series.tooltip.background.strokeWidth = 0;

                // Tooltip text coloring
                series.tooltip.autoTextColor = false;
                series.tooltip.label.fill = am4core.color("#000");

                // Set up data fields
                series.dataFields.type = "type";
                series.dataFields.url = "url"
                series.dataFields.name = "name";
                series.dataFields.children = "children";
                series.dataFields.id = "cluster_num";

                // Add labels
                series.nodes.template.label.text = "{cluster_num}";

                // TODO: clean out commented out stuff
                //series.fontSize = 10;
                series.minRadius = 25.9;
                series.maxRadius = 30;
                series.rootEmSize = 3;
                //series.nodes.template.label.valign = "bottom";
                //series.nodes.template.label.fill = am4core.color("#000");
                //series.nodes.template.label.dy = 10;

                // Configure icons
                let icon = series.nodes.template.createChild(am4plugins_bullets.PinBullet);
                icon.image = new am4core.Image();
                icon.image.propertyFields.href = "image_url";
                icon.horizontalCenter = "middle";
                icon.verticalCenter = "middle";
                icon.circle.radius = am4core.percent(100);
                icon.circle.strokeWidth = 0;
                icon.background.pointerLength = 0;
                icon.background.disabled = true;

                // The gravitational strength of the center of the chart
                series.centerStrength = 1.5;

                this.series = series
            }
        },

        data() {
            return {
                chart: null,
                series_data: []
            }
        },
        mounted() {
            this.initGraph();
        }
    }

</script>

<style scoped>
    .cluster-graph {
        height: 100vh;
        width: 100vw;
        background: black;
    }

</style>