function setUpPebMedids(pubmedIds, container) {
  if(pubmedIds == " ")
    return true;
  var ids = pubmedIds.split(';')

  
  for( var index in ids) {
    $('#' + container).append("<span class='attribution'><span class='attributionHeader'></span>Pubmed:" + ids[index] + "</span>");
  }
  return true;
}

function setUpPathwayTable(superPathway, nodeId) {
  //if(superPathway.length > 0) {
    var count = 0
    $("#pathwayTable  tr:not(:first)").html(""); 
    for(var index in superPathway){
      $('#pathwayTable').append( 
        "<tr>" +
          "<th class='gene-abstrct-info' >" + superPathway[index]['SuperPathwayName'] + "</th>" +
          "<td class='gene-abstrct-info'>" + superPathway[index]['GenesCount'] + "</td>" +
          "<td class='gene-abstrct-info'>" + superPathway[index]['RelevanceScore'] + "</td>" +
        "</tr>"
      );
      count += 1;
    }
    $('#help-text-detail-pathway').text(count +  " search results for " + nodeId);
    $("#pathwayTable").show();
    return true;
  //}
}

function setUpDiseaseTable(diseases, nodeId) {
  var diseasesCount = 0;
  for(var i in diseases) {
    if(i == 'null')
      continue;

    $('#diseaseTable').append(
      "<tr>" + 
        "<th><span class='attribution'><span class='attributionHeader'></span>" + diseases[i] + "</span></th>" +
        "<td class='gene-abstrct-info'>" + i + "</td>" +
      "</tr>"
    );
    diseasesCount += 1;
  }

  $('#help-text-detail-disease').text(diseasesCount +  " search results for " + nodeId);
  return diseasesCount;
}

function setUpDrugTable(drugs, nodeId) {
  
  var count = 0;
  for(var i in drugs) {
    $('#drugList').append("<li><a>" + i +"</a><span class='attribution'><span class='attributionHeader'></span>Source：" + drugs[i] + "</span></li>");
    count += 1;
  }
   $('#help-text-detail-drug').text(count +  " search results for " + nodeId);
   $('#help-text-detail-drug').show();
   
   return true;
}

function setUpNodeTable(nodeId) {
  $('#help-text-detail-drug').hide();
  DoAjax(nodeId);
  loadDrug(nodeId);
  $('#gene-title').text(nodeId);
  $("tr#"+nodeId).show();
  $('#UniProtID a').text(nodeId);
}

function setUpRightMenu (cy) {
  // body...
  cy.contextMenus({
    menuItems: [
      {
        id: 'remove',
        title: 'Delete selected node',
        selector: 'node, edge',
        onClickFunction: function (event) {
          event.cyTarget.remove();
        },
        //hasTrailingDivider: true
      },
      {
        id: 'hide',
        title: 'Hide selected node',
        selector: '*',
        onClickFunction: function (event) {
          event.cyTarget.hide();
        },
        disabled: false,
        hasTrailingDivider: true
      },
      {
        id: 'add-node',
        title: 'Add a node',
        coreAsWell: true,
        onClickFunction: function (event) {
          var data = {
              group: 'nodes'
          };
          
          cy.add({
              data: data,
              position: {
                  x: event.cyPosition.x,
                  y: event.cyPosition.y
              }
          });
        }
      },
      {
        id: 'remove-selected',
        title: 'Delete selected node',
        coreAsWell: true,
        onClickFunction: function (event) {
          cy.$(':selected').remove();
        }
      },
      {
        id: 'link kegg',
        title: 'Link to KEGG database',
        selector: 'node',
        onClickFunction: function (event) {
          var evtTarget = event.cyTarget;
          if (evtTarget.id() != 'undefined') {
            linkUrl = "http://www.kegg.jp/dbget-bin/www_bfind_sub?mode=bfind&max_hit=1000&dbkey=kegg&keywords=" + evtTarget.id();
            window.open(linkUrl);
          }
        }
      },
      {
        id: 'link common Pathway',
        title: ' Link to Pathway common Database',
        selector: 'node',
        onClickFunction: function (event) {
          var evtTarget = event.cyTarget;
          if (evtTarget.id() != 'undefined') {
            linkUrl = "http://www.pathwaycommons.org/pc/webservice.do?version=3.0&snapshot_id=GLOBAL_FILTER_SETTINGS&record_type=PATHWAY&q="+evtTarget.id()+"&format=html&cmd=get_by_keyword"
            window.open(linkUrl);
          }
        }
      },
      {
        id: 'link reactome',
        title: 'Link to Reactome Database ',
        selector: 'node',
        onClickFunction: function (event) {
          var evtTarget = event.cyTarget;
          if (evtTarget.id() != 'undefined') {
            linkUrl = "http://www.reactome.org/content/query?q="+event.cyTarget+"&species=Homo+sapiens&species=Entries+without+species&cluster=true"
            window.open(linkUrl);
          }
        }
      },
      {
        id: 'link wikipathways',
        title: 'Link to Wikipathways Database',
        selector: 'node',
        onClickFunction: function (event) {
          var evtTarget = event.cyTarget;
          if (evtTarget.id() != 'undefined') {
            linkUrl = "http://www.wikipathways.org//index.php?query="+event.cyTarget+"&title=Special%3ASearchPathways&doSearch=1&sa=Search"
            window.open(linkUrl);
          }
        }
      },
    ],
    menuItemClasses: ['custom-menu-item'],
    contextMenuClasses: ['custom-context-menu']
  });//end-menu
}

    
function setUpNetworkStatistics(cy) {
  
} 

function getTotalInOutDegree(nodes) {
  var indegree = 0;
  var outdegree = 0;
  for(var i=0; i < nodes.length; i++){
    indegree += nodes[i].indegree();
    outdegree += nodes[i].outdegree();
  }
  var result = {}
  result['totalInDegree'] = indegree;
  result['totalOutDegree'] = outdegree;
  return result;
}

function getDegreeDistribute(CytoscapeObject) {
  var degreeDis = new Object();
  var nodes = CytoscapeObject.filter('node');
  for(var i = 0; i < nodes.length ; i++){
    var degree = nodes[i].degree();
    if(degree in degreeDis) {
      degreeDis[degree] += 1;
    } else {
      degreeDis[degree] = 1
    }
  }
  return degreeDis;
}

function setUpFrameUrl(nodeId)
{
  var expImgUrl = "http://genecardsdata.blob.core.windows.net/rna-expression-v470/gene_expression_" + nodeId + ".png"
  $('#expImg').attr("src", expImgUrl);
  $('#curgene').text(nodeId);
}