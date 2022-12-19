(function ($) {
    Drupal.behaviors.multiExpandAccordion = {
            attach:function (context, settings) {            	
            	$('#accordion .head').click(function() {
            	      $(this).next().toggle();
            	      $(this).toggleClass("collapsed");
            	      $(this).toggleClass("open");
            	      return false;
            	}).toggleClass("collapsed");   
            	
            	$('.expand_all').click(function() {
            		if($(this).hasClass("collapse_all")){
            		  $('#accordion .open').click();
              	      $('.expand_all').removeClass("collapse_all");
              	      $('.expand_all').html("Expand All");
            		}
            		else{
	          	      $('#accordion .collapsed').click();
	          	      $('.expand_all').addClass("collapse_all");
	          	      $('.expand_all').html("Collapse All");
            		}
          	      return false;
            	}); 
            	$('#accordion .head').first().click();
            	$('#accordion .openOnLoad').click();
            }
        }
    
 /*   Drupal.behaviors.showMorePopup = {
            attach:function (context, settings) {    
            	$('.subTopicMoreLink').click(function() {
            		 var dialog = $("#dialog");
                     if ($("#dialog").length == 0) {
                         dialog = $('<div id="dialog" style="display:none"></div>').appendTo('body');
                     }
                     var parentWidth = $(this).prev().width();
                     // load remote content
                     dialog.load(
                             "print/node/1363",
                             {},
                             function (responseText, textStatus, XMLHttpRequest) {
                                 dialog.dialog({
                                     position:"top",
                                     width:800,
                                     modal:true
                                 });
                             }
                         );            		
          	    	return false;
            	});  
            }
        }*/
    Drupal.behaviors.facetShowMore = {
            attach:function (context, settings) {    
            	$('.facetShowMore').click(function() {
            		$(this).parent().find('.hiddenFacetItem').toggle();
            		if($(this).text() == "Show More"){
            			$(this).text("Show Less");
            		}else{
            			$(this).text("Show More");
            		}
          	    	return false;
            	});  
            }
        }    
    
    Drupal.behaviors.pagerActions = {
            attach:function (context, settings) {                	
            	$('.pagerSizeSelect').change(function() {
            		var newURL = updateURLParameter(window.location.href, 'items_per_page', $(this).attr("value"));
            		window.location.href = newURL;
            	});  
            	$('.sortBySelect').change(function() {
            		var newURL = updateURLParameter(window.location.href, 'sort_by', $(this).attr("value"));
            		window.location.href = newURL;
            	});
            	$('.tableSortHeader').click(function() {
            		var newURL = updateURLParameter(window.location.href, 'sort_by', $(this).attr("value"));
            		if($(this).hasClass("ASC")){
            			newURL = updateURLParameter(newURL, 'sort_order', "DESC");
            		}else{
            			newURL = updateURLParameter(newURL, 'sort_order', "ASC");
            		}
            		window.location.href = newURL;
            		return false;
            	});

            }
        }
    

    
    Drupal.behaviors.autocomplete = {
    		attach:function (context, settings) { 
	    		$("#searchInput" ).autocomplete({
	                position: { my: "right top", at: "right bottom" },
	                minLength: 0,
	                source:function(request, response) {
	                    $.getJSON("/smart_search/autocomplete", { selected: $('input[name=searchType]:checked').attr("id"), term: $('input[name=searchText]').val() }, response);
	                },
	                focus: function (event, ui) {
	                        $(event.target).val(ui.item.label);
	                        return false;
	                },
	                select: function (event, ui) {
	                        $(event.target).val(ui.item.label);
	                        window.location = ui.item.url;
	                        return false;
	                }
	    		});
    		}
    }
    

}(jQuery));


(function ($) {
    $(document).ready(function() {
// *********** data tables style - begin ******** //
        $("table.datatable > thead tr").addClass('header');
        $("table.datatable > tbody tr:even").addClass('even');
        $("table.datatable > tbody tr:odd").addClass('odd');
        ﻿$("ul").each(function(){
            $this = $(this);
            $this.children("li:even").addClass("even").nextUntil("li").addClass("even");
            $this.children("li:odd").addClass("odd").nextUntil("li").addClass("odd");
        });
// ********** data tables style - end ******* //
// ********** faq tabs - begin ******* //
        $(".faq_content").hide(); //Hide all content
        $("ul.faqs li:first").addClass("active").show(); //Activate first tab
        $(".faq_content:first").show(); //Show first tab content
        //faq - On Click Event
        $("ul.faqs li").click(function() {
            $("ul.faqs li").removeClass("active"); //Remove any "active" class
            $(this).addClass("active"); //Add "active" class to selected tab
            $(".faq_content").hide(); //Hide all tab content
            var activeTab = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
            $(activeTab).fadeIn(); //Fade in the active content
            return false;
        });
// ********** faq tabs - end ******* //
// ********** collapse content - begin ******* //
        $("div.expContent").hide();
        $("ul#contentCollapse li:first div.expContent").show();
        $("ul#contentCollapse li:first h3 span").addClass('expanded');
        $("h3.expLink").click(function() {
            var that = this;
            $(".expContent:visible").slideUp("slow");
            $(".expLink span.expanded")
                .removeClass('expanded')
                .addClass('collapsed');
            $(this)
                .next(".expContent:hidden")
                .slideDown("slow", function(){
                    $('span.collapsed', that)
                        .removeClass('collapsed')
                        .addClass('expanded');
                });
        });
// ********** collapse content - end ******* //
    });
}(jQuery));





/**
 * http://stackoverflow.com/a/10997390/11236
 */
function updateURLParameter(url, param, paramVal){
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}




function applySearchFilters(){
	jQuery('.facetMainTitle').append("<div class='processing'><span>Loading Page</span></div>");
    jQuery('input[type=checkbox]').attr("disabled", true);	
    var cUrl = prepareSearchFilterUrl();
    window.location.href = cUrl; 
}

/**
*  Returns the search URL
*  Requires 'getSearchFilterCriteria' function
*/

function prepareSearchFilterUrl(){
    var page_size = getSearchFilterCriteria('items_per_page');
    var searchTerm = '';
    var cUrl = null;
    var qsParm = getQuerystringValues();
    
    searchTerm = ""
    if(!qsParm){
        searchTerm = "";
    }else if(qsParm["searchText"]){        
        searchTerm = qsParm["searchText"];
    }    
    cUrl = "sbir_search?searchText=" + searchTerm ;
    
    if(qsParm["searchTextType"]){
    	cUrl = cUrl + "&searchTextType=" + qsParm["searchTextType"] ;	
    }
    
    if(qsParm["searchType"]){
    	cUrl = cUrl + "&searchType=" + qsParm["searchType"] ;	
    }
    if(qsParm["solicitation_nid"]){
    	cUrl = cUrl + "&solicitation_nid=" + qsParm["solicitation_nid"] ;	
    }
    
    if(qsParm["searchTextField%5Bsubtopic%5D"]){
    	cUrl = cUrl + "&searchTextField[subtopic]=subtopic";	
    }
    if(qsParm["searchTextField%5Bdescription%5D"]){
    	cUrl = cUrl + "&searchTextField[description]=description";	
    }
    
    (function ($) {
    	$.each( $('.facetHeading'),
    			function(index,value){
    				var facet_id = $(value).attr('facetid');
    				var facet_value= getSearchFilterCriteria(facet_id);
    				cUrl += facet_value;
    			}
    	);
    }(jQuery));
    if(page_size){
    	cUrl +=page_size;
        //cUrl += "&items_per_page=" + encodeURIComponent(page_size) ;
    } 
    return cUrl;
}



/**
 *  Returns the selected filter parameters on the form
 * @param filterName
 */
    function getSearchFilterCriteria(filterName){
        var filterId = '';
        var oFilterIds = document.getElementsByName(filterName);
        if(!eval(oFilterIds)){
            return filterId;
        }
        for(var i = 0; i < oFilterIds.length; i++)
        {
            if(oFilterIds[i].checked)
            {
               /* if(filterId.length>0){
                    filterId = filterId  + '~' + oFilterIds[i].value;
                }else{
                    filterId = oFilterIds[i].value;
                }*/
            	filterId += '&' + filterName + '[]=' + encodeURIComponent(oFilterIds[i].value);
            }
        }

        return filterId;
    }
    
    
    function getQuerystringValues() {
        var qsParm = new Array();
        var query = window.location.search.substring(1);
        var parms = query.split('&');
        for (var i=0; i<parms.length; i++) {
            var pos = parms[i].indexOf('=');
            if (pos > 0) {
                var key = parms[i].substring(0,pos);
                var val = parms[i].substring(pos+1);
                qsParm[key] = val;
            }
        };
        return qsParm;
    }

   