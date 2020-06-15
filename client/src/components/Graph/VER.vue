<template>
  <div class="erWrapper">
    <div id="myDiagramDiv" style="border: solid 1px black; width:100%; height: 100% !important;"></div>
  </div>
</template>


<script>
import go from 'gojs'

import { GuidedDraggingTool } from 'gojs/extensionsTS/GuidedDraggingTool.ts'
import { mapGetters } from 'vuex'

import reqsMixin from '../../mixins/reqsMixin'

const $ = go.GraphObject.make;

export default {
  name: 'VER',
  mixins: [reqsMixin],
  data() {
    return {
      myDiagram: null,
    }
  },
  mounted() {
    this.myDiagram = $(go.Diagram, 'myDiagramDiv',
      {
        'undoManager.isEnabled': true,
        layout: $(go.LayeredDigraphLayout, {
          columnSpacing: 100,
          layerSpacing: 200,
          layeringOption: go.LayeredDigraphLayout.LayerLongestPathSource,
        }),
        autoScale: go.Diagram.Uniform,
        initialAutoScale: go.Diagram.Uniform,
      }),
    this.myDiagram.nodeTemplate = $(go.Node, 'Auto',
      $(go.Shape, { fill: 'white' }),
      $(go.Panel, 'Table',
        {
          stretch: go.GraphObject.Fill,
          minSize: new go.Size(100, 10),
        },
        new go.Binding('itemArray', 'attrs'),
        $(go.RowColumnDefinition,
          { row: 0, background: '#2d7ef7' }),
        $(go.RowColumnDefinition,
          { row: 1, separatorStroke: 'black' }),
        // the table headers -- remains even if itemArray is empty
        $(go.Panel, 'TableRow',
          { isPanelMain: true },
          new go.Binding('itemArray', 'columnDefinitions'),
          {
            itemTemplate: // bound to a column definition object
                $(go.Panel, 'Auto',
                  new go.Binding('column'),
                  $(go.TextBlock,
                    {
                      alignment: go.Spot.Center,
                      margin: new go.Margin(8, 8, 8, 8),
                      stroke: 'white',
                      font: 'bold 14pt sans-serif',
                      textAlign: 'center',
                      minSize: new go.Size(100, NaN),
                      maxSize: new go.Size(NaN, NaN),
                    },
                    new go.Binding('text'))),
          }),
        {
          defaultAlignment: go.Spot.Left,
          defaultColumnSeparatorStroke: 'black',
          itemTemplate:
              $(go.Panel, 'TableRow',
                new go.Binding('itemArray', 'columns'),
                {
                  itemTemplate:
                    $(go.Panel, 'Auto',
                      { stretch: go.GraphObject.Fill, alignment: go.Spot.Center },
                      new go.Binding('column', 'attr',
                        ((a, elt) => {
                          const cd = findColumnDefinitionForName(elt.part.data, a);
                          if (cd !== null) return cd.column;
                          throw new Error(`unknown column name: ${a}`);
                        })),
                      $(go.TextBlock, 'stretch: Horizontal',
                        {
                          margin: new go.Margin(5, 5, 5, 5),
                          wrap: go.TextBlock.None,
                          minSize: new go.Size(100, NaN),
                          maxSize: new go.Size(NaN, NaN),
                          textAlign: 'left',
                          alignment: go.Spot.Center,
                          wrap: go.TextBlock.WrapFit,
                        },
                        new go.Binding('isUnderline', 'isKey'),
                        new go.Binding('text').makeTwoWay())),
                }),
        }))

    this.myDiagram.linkTemplate = $(go.Link, {
      resegmentable: false,
    },
    $(go.Shape),
    $(go.Shape, { toArrow: 'Standard' }),
    $(go.TextBlock, new go.Binding('text', 'text'),
      {
        segmentOffset: new go.Point(0, -10),
        segmentOrientation: go.Link.OrientUpright,
      }),
    $(go.TextBlock, new go.Binding('text', 'fromS'),
      { segmentOffset: new go.Point(0, -10), segmentIndex: 1, segmentFraction: 0.15 }),
    $(go.TextBlock, new go.Binding('text', 'toO'),
      { segmentOffset: new go.Point(0, -10), segmentIndex: 1, segmentFraction: 0.9 }));

    this.updateDiagram()
  },
  computed: {
    ...mapGetters({
      er: 'ergeneration/getER',
    }),
  },
  methods: {
    updateDiagram() {
      this.myDiagram.model = $(go.GraphLinksModel,
        {
          copiesArrays: true,
          copiesArrayObjects: true,
          nodeDataArray: this.getNodeData(),
          linkDataArray: this.getLinkData(),
        });
    },
    getNodeData() {
      return Object.entries(this.er).map((e, idx) => ({
        key: idx + 1,
        columnDefinitions: [
          // each column definition needs to specify the column used
          { attr: 'text', text: e[0], column: 0 },
        ],
        attrs: e[1].attrs.map((a) => ({
          columns: [{
            attr: 'text',
            text: a.text,
            isKey: a.isKey,
          }],
        })),
      }))
    },
    getLinkData() {
      const links = []
      Object.entries(this.er).forEach((e) => {
        e[1].rels.forEach((r) => {
          links.push({
            from: this.getNodeData().find((n) => n.columnDefinitions[0].text === e[0]).key,
            to: this.getNodeData().find((n) => n.columnDefinitions[0].text === r.to).key,
            text: r.isBetweenAttrs ? `${this.translateNum(r.fromNum, r.rel.mandatory)}        ${r.rel.text}(${r.fromAtr})        ${this.translateNum(r.toNum, true)}`
              : `${this.translateNum(r.fromNum, r.rel.mandatory)}        ${r.rel.text}       ${this.translateNum(r.toNum, true)}`,
            // fromS: this.translateNum(r.fromNum, r.rel.mandatory),
            // toO: this.translateNum(r.toNum, true),
          })
        })
      })
      return links
    },
  },
}
</script>

<style lang="scss">
.erWrapper {
  height: 70vh;
}
</style>
