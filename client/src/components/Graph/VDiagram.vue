<template>
  <div id="myDiagramDiv" style="border: solid 1px black; width:100%; height: 30vh;"></div>
</template>


<script>
import go from 'gojs';

import { GuidedDraggingTool } from 'gojs/extensionsTS/GuidedDraggingTool.ts';

import reqsMixin from '../../mixins/reqsMixin'

const $ = go.GraphObject.make;

export default {
  name: 'VDiagram',
  props: {
    sent: {
      type: Object,
      default() {
        return {}
      },
    },
  },
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
        layout: $(go.TreeLayout,
          {
            nodeSpacing: 100,
            layerSpacing: 200,
          }),
      })
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
        { // the rows for the people
          defaultAlignment: go.Spot.Left,
          // defaultRowSeparatorStroke: "black",
          defaultColumnSeparatorStroke: 'black',
          itemTemplate: // bound to a person/row data object
              $(go.Panel, 'TableRow',
                // which in turn consists of a collection of cell objects,
                // held by the "columns" property in an Array
                new go.Binding('itemArray', 'columns'),
                // you could also have other Bindings here for the whole row
                {
                  itemTemplate: // bound to a cell object
                    $(go.Panel, 'Auto', // each of which as "attr" and "text" properties
                      { stretch: go.GraphObject.Fill, alignment: go.Spot.Center },
                      new go.Binding('column', 'attr',
                        ((a, elt) => {
                          const cd = findColumnDefinitionForName(elt.part.data, a);
                          if (cd !== null) return cd.column;
                          throw new Error(`unknown column name: ${a}`);
                        })),
                      // you could also have other Bindings here for this cell
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
                        new go.Binding('text').makeTwoWay(),
                        new go.Binding('isUnderline', 'isKey'))),
                }),
        }))

    this.myDiagram.linkTemplate = $(go.Link,
      $(go.Shape), // this is the link shape (the line)
      $(go.Shape, { toArrow: 'Standard' }), // this is an arrowhead
      $(go.TextBlock, new go.Binding('text', 'text'),
        {
          segmentOffset: new go.Point(0, -10),
          segmentOrientation: go.Link.OrientUpright,
        }),
      $(go.TextBlock, new go.Binding('text', 'fromS'),
        { segmentIndex: 0, segmentFraction: 0.2, segmentOffset: new go.Point(20, 20) }),
      $(go.TextBlock, new go.Binding('text', 'toO'),
        { segmentIndex: -1, segmentFraction: 0.2, segmentOffset: new go.Point(-20, 20) }));

    this.updateDiagram()
  },
  watch: {
    sent: {
      handler() {
        this.updateDiagram()
      },
      deep: true,
    },
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
    entities() {
      let entities = []
      if (this.sent.objs.type === 'ent') {
        entities = entities.concat(this.sent.objs.objects)
      }

      if (this.sent.subjs.type === 'ent') {
        entities = entities.concat(this.sent.subjs.subjects)
      }
      return entities
    },
    attrs() {
      let attrs = []
      if (this.sent.objs.type === 'atr') {
        attrs = attrs.concat(this.sent.objs.objects)
      }

      if (this.sent.subjs.type === 'atr') {
        attrs = attrs.concat(this.sent.subjs.subjects)
      }
      return attrs
    },
    getNodeData() {
      return this.entities().map((e, idx) => ({
        key: idx + 1,
        columnDefinitions: [
          // each column definition needs to specify the column used
          { attr: 'text', text: e.text, column: 0 },
        ],
        attrs: this.attrs().map((a) => ({
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
      if (this.sent.subjs.subjects.length > 0
        && this.sent.subjs.type === 'ent'
        && this.sent.objs.objects.length > 0
        && this.sent.objs.type === 'ent') {
        this.sent.subjs.subjects.forEach((s) => {
          this.sent.objs.objects.forEach((o) => {
            links.push({
              from: this.getNodeData().find((n) => n.columnDefinitions[0].text === s.text).key,
              to: this.getNodeData().find((n) => n.columnDefinitions[0].text === o.text).key,
              text: this.sent.dep.text,
              fromS: this.translateNum(s.num, this.sent.dep.mandatory),
              toO: this.translateNum(o.num, true),
            })
          })
        })
      }

      return links
    },
  },
}
</script>
