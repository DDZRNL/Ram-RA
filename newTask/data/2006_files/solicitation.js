(function ($) {
  $(document).ready(function() {

    $('#goto8').click(function(){
      $('#li-checklist').find('ul').slideToggle();
      $('#li-checklist').addClass('expanded');
      return false;
    });
	
	$('a[href="#"]').click(function(e) {
		e.preventDefault(); 
	}); 
  setTimeout(scrollTopicOnLoad, 1500);

	
	$("a.pointerScrollLinkFA").click(function(evt){
    var pathname = window.location.pathname;
	  var divId = '#fa_' + $(this).attr('id').replace("pointer_","");
    topicfromURL = getParameterByName('topic');
    if(topicfromURL){
      divId = topicfromURL;
    }
    var getValue_SBIR = $("input[name=prg_SBIR]").val();
    var getValue_STTR = $("input[name=prg_STTR]").val();
    current_page = '';
    if(pathname.search(getValue_SBIR) > 0){
      current_page = 'SBIR';
    }
    else{
      current_page = 'STTR';
    }
    if($(divId).length > 0){
      $(divId).closest('a.expandable-list').parent().addClass('topic-collapsed');
      $(divId).closest('div.expandable-content').fadeIn();
      $('html, body').animate({
        scrollTop: $(divId).offset().top-100
      }, 500);
      return false;
    }
    else{
      if(current_page == 'SBIR'){
        url = window.location.origin + "/solicit/" + getValue_STTR + "/detail?data=ch9&topic=" + divId.replace('#', '');
      }
      else{
        url = window.location.origin + "/solicit/" + getValue_SBIR + "/detail?data=ch9&topic=" + divId.replace('#', '');
      }
      window.open(url, '_blank');      
    }
	});
	
	$("a.pointerScrollLinkMD").click(function(evt){
    var pathname = window.location.pathname;
	  var divId = '#md_' + $(this).attr('id').replace("pointer_","");
    topicfromURL = getParameterByName('topic');
    if(topicfromURL){
      divId = topicfromURL;
    }
    var getValue_SBIR = $("input[name=prg_SBIR]").val();
    var getValue_STTR = $("input[name=prg_STTR]").val();
    current_page = '';
    if(pathname.search(getValue_SBIR) > 0){
      current_page = 'SBIR';
    }
    else{
      current_page = 'STTR';
    }
    if($(divId).length > 0){
      $(divId).closest('a.expandable-list').parent().closest('a.expandable-list').parent().addClass('topic-collapsed');
      $(divId).closest('div.expandable-content').parent().closest('div.expandable-content').fadeIn();
      $(divId).closest('a.expandable-list').parent().addClass('topic-collapsed');
      $(divId).closest('div.expandable-content').fadeIn();
      //$(divId).closest('a.expandable-list').trigger('click');
      $('html, body').animate({
        scrollTop: $(divId).offset().top-100
      }, 500);
      return false;
    }
    else{
      if(current_page == 'SBIR'){
        url = window.location.origin + "/solicit/" + getValue_STTR + "/detail?data=ch9&topic=" + divId.replace('#md', 'fa');
      }
      window.open(url, '_blank');      
    }
	});

    $('#goto_appendecies').click(function(){
      $('#li-appendices').find('ul').slideToggle();
      $('#li-appendices').addClass('expanded');
      return false;
    });

    // subchapters link
    if ($('a.subchapters').length > 0) {
      $('a.subchapters').click(function() {
       //alert($(this).text());
        $('html, body').animate({
                scrollTop: $('[name="' + $(this).text() + '"]').offset().top
            }, 500);
            return false;
      });
    }

    // chapter 9 taxonomy containers are there
    if ($('div.txnmy-container').length > 0) {

        if ($('a.tab-selected').length == 0) {
        // md anchor is selected
          $('a.txnmy-tab:first').addClass('tab-selected');
          $('div.txnmy-container:first').addClass('container-selected');

          if ($('div.txnmy-container').length == 2) {
           // str container is hidden
           $('div.txnmy-container:last').hide();
          }
        }
        else {
          $('div.txnmy-container:first').hide();
        }

        $('.txnmy-tab').click(function() {
          // hide
          $('.container-selected').hide();
          $('.container-selected').removeClass('.container-selected');
          if($('#it_is_sttr').length > 0){
        	  $('.tab-selected').css('border-bottom','');
          }
          $('.tab-selected').removeClass('tab-selected');
          

          // display selected taxonomy content
          $('#div-container-'+$(this).attr('id')).fadeIn(); //slideToggle();
          $('#div-container-'+$(this).attr('id')).addClass('container-selected');
          $(this).addClass('tab-selected');
          if($('#it_is_sttr').length > 0){
        	  $(this).css('border-bottom','24px solid orange');
          }
          // alter print url
          alter_print_path($(this).attr('id'));
          return false;
        });


      // hidden all topics which has long length
      $('div.whole-topic-content').hide();

      // add read-more
      $('a.read-more').click(function(){
        // hidden short content
        $(this).closest('p.parsed-topic-content').hide();
        $(this).closest('p.parsed-topic-content').siblings('div.whole-topic-content').fadeIn();
        return false;
      });

      // read less
      $('a.read-less').click(function(){
        // hidden short content
        $(this).closest('div.whole-topic-content').hide();
        $(this).parent().siblings('p.parsed-topic-content').fadeIn();
        return false;
      });

      // expand left navigation chapters
    }

  // left navigation default
  $('.solicitation-left-navigation li:not(:has(ul))').addClass('not-expandable');
  $('.solicitation-left-navigation li:has(ul)').addClass('collapsed');
  $('.solicitation-left-navigation .collapsed').find('ul').hide();

  $('.solicitation-left-navigation .collapsed a').click(function(event){
    if (this == event.target) {
      if ($(this).attr('href') == '#'){
        $(this).parent().children('ul').slideToggle();
        $(this).parent().addClass('expanded');
        // if there is any expanded and it doesn't have same parent, set to collapsed
       /*  if ($(this).parent().find('> ul.expanded').length == 0) {
          $('.solicitation-left-navigation .expanded').find('ul').hide('slow');
          $('.solicitation-left-navigation .expanded').addClass('collapsed');
          $('.solicitation-left-navigation .expanded').removeClass('expanded');
        }*/
        return false;
      }
    }
  });

  set_active_menu_class();

  $('a.expandable-list').click(function(){

    if ($(this).parents('li').first().hasClass('topic-collapsed')){
      $(this).parent().siblings('div.expandable-content').fadeOut();
      $(this).parents('li').first().removeClass('topic-collapsed'); // expanded li got class
      $(this).parent().removeClass('topic-collapsed');

      // need alert if it has child expand anchor
      /*var $child = $(this).parent().siblings('div.expandable-content').find('a.expandable-list');
      if ($('#it_is_sbirselect').length > 0 && $child.length > 0 ) {
        $child.trigger('click');
      }*/
    }
    else {
      $(this).parent().siblings('div.expandable-content').fadeIn();
      $(this).parents('li').first().addClass('topic-collapsed'); // expanded li got class
      $(this).parent().addClass('topic-collapsed');

      // need alert if it has child expand anchor
      var $child = $(this).parent().siblings('div.expandable-content').find('a.expandable-list');
      if ($('#it_is_sbirselect').length > 0 && $child.length > 0 ) {
        $child.trigger('click');
      }
    }

    return false;
  });

  // expand all. collapse all
  $('a.expand-all').click(function() {
    // expand all
    if (!$(this).parent().hasClass('collapse-all')) {
      $('a.expandable-list').parent().addClass('topic-collapsed');
      $('div.expandable-content').fadeIn();
      $('a.expand-all').text('Collapse All');
      $('a.expand-all').parent().addClass('collapse-all');
      $('a.expand-all').parent().removeClass('expand-all');
    }
    else {
      $('a.expandable-list').parent().removeClass('topic-collapsed');
      $('div.expandable-content').fadeOut();
      $('a.expand-all').text('Expand All');
      $('a.expand-all').parent().addClass('expand-all');
      $('a.expand-all').parent().removeClass('collapse-all');
    }
    return false;
  });

  // md on the list anchors need to trigger on the right
  $('.left-md-anchor').click(function() {
    // close everything
    $('div.expandable-content').fadeOut();
    $('a.expand-all').text('Expand All');
    $('a.expand-all').parent().addClass('expand-all');
    $('a.expand-all').parent().removeClass('collapse-all');
    $('.topic-collapsed').removeClass('topic-collapsed');

    // look for taxonomy on the right
    $('a.right-md-' + $(this).attr('id')).parent().siblings('a.expandable-list').trigger('click');
  });

  $('.appendix-control').addClass('hidden');

  $('.a_appendices').click(function() {
     $('.appendix-control').each(function() {
        if ($(this).hasClass('hidden'))
        {
          $(this).removeClass('hidden');
        }
        else {
          $(this).addClass('hidden');
        }
     });
      return false;
   });

    $('a.qa-icon').click(function() {
     //$(this).parents('ul').first().siblings('a.subtopic-qa').focus();
      $(this).parents('div').siblings('a.subtopic-qa').trigger('click');
      return false;
    });

    if ($('.subtopic-qa').length > 0) {

      $('.subtopic-qa').click(function(event){

        var current_topic_nid = $(this).siblings('p.topic_nid').html();
        var aq_anchor = $(this);
        aq_anchor.hide();
        // looking for QA form container
          var qaURL = location.protocol + '//' + location.host + '/solicitation-qa-json/' + current_topic_nid;
          $.getJSON(qaURL, {}, function(data){
            // add form into container
            aq_anchor.next().append(data.returnform);
            // display form
            aq_anchor.next().fadeIn();

            // qa should've send
            $('.qa_form_submit').click(function() {

              var qaSubmitURL = location.protocol + '//' + location.host + '/solicitation-qa-submit-json/' + encodeURIComponent($('#-sbir-solicitation-qa-form').serialize());

              $.getJSON(qaSubmitURL, {}, function(data) {
                if (data.status) {
                  // display success message, remove form
                  aq_anchor.next().hide();
                  aq_anchor.next().html(data.message);
                  aq_anchor.next().fadeIn();
                }
                else {
                  // display error message
                  aq_anchor.next().find('div.err').remove();
                  aq_anchor.next().append(data.message);
                }
                return;
              });
              return false;
            });

          });

        return false;
      });
    }
      // hide some elements
      $('p.topic_nid').hide();
      // qa form container
      $('div.qa-form-container').hide();
      // hide expanded content
      $('div.expandable-content').hide();

      // expand subtopic functionality
      if ($('#need_to_open_topic').length > 0||$('#need_to_open_subtopic').length>0) {
      	var topic_control;
  		if($('#need_to_open_topic').length > 0) {
  			topic_control = $("[href*='/printpdf/" + $('#need_to_open_topic').val() + "']");
  		}
      	
    	if($('#need_to_open_subtopic').length > 0) {
    		var subtopicId = '#'+'subtopic_' + $('#need_to_open_subtopic').val();
    		topic_control = $(subtopicId);
    	}
    	
    	var expanding_content = topic_control.parents('div.expandable-content');
  		
  			if (topic_control.parents('div.topicHeader').length > 0) {
  			  // topic
  			  topic_control.parents('.expandable-content').siblings('div.taxonomyTopic').addClass('topic-collapsed');
  			  topic_control.parents('li.md-taxonomy').first().addClass('topic-collapsed');
  			}
  			else {
  			  // suptopic opened
  			  expanding_content.siblings('div.topicHeader').addClass('topic-collapsed');
  			  expanding_content.parents('li.first-topic').addClass('topic-collapsed');

  			  expanding_content.parents('.expandable-content').siblings('div.taxonomyTopic').addClass('topic-collapsed');
  			  topic_control.parents('li.md-taxonomy').first().addClass('topic-collapsed');
  			  expanding_content.siblings('div.taxonomyTopic').addClass('topic-collapsed');
  			}
  			expanding_content.show();
  			$('html, body').animate({
  						  scrollTop: topic_control.offset().top-200
  		  }, 500);
  			
        }
      //scroll down and open focus area from EHB
      if($('#need_to_open_topicnum').length > 0) {
      		var topicId = '#'+'fa_' + $('#need_to_open_topicnum').val();
      		topic_control = $(topicId);
      		topic_control.siblings('a.expandable-list').trigger("click");
      		$('html, body').animate({
				  scrollTop: topic_control.offset().top-200
      		}, 500);
      }
    

      // expand STTR topics
      if ($('#need_to_open_topic').length <= 0 && $('#need_to_open_topicnum').length <= 0 && $('#need_to_open_subtopic').length<=0 && $('#it_is_sttr').length > 0) {
          $('a.expandable-list').first().trigger('click');
         // alert('it is triggered');
      }
      if($('#it_is_sttr').length > 0){
    	  $('.tab-selected').css('border-bottom','24px solid orange');
      }
    function set_active_menu_class() {

      var q_data = getParameterByName('data');
      var q_l1 = getParameterByName('l1');
      var q_l2 = getParameterByName('l2');
      if (q_data.length > 0) {
        // set class for active
        if (q_data != 'ch9'){
          $("[href*='?data=" + q_data +"']").addClass('active');
        }
        else{
          var q_s = getParameterByName('s');
          var active_data_anchor = $("[href='?data=" + q_data +"&s=" + q_s + "']");
          var data_anchor = $("[href^='?data=" + q_data + "']");
          data_anchor.closest('ul').show();
          data_anchor.siblings('ul').show();
          if (active_data_anchor.length == 2) {
              active_data_anchor.last().addClass('active');
          }
          else {
              active_data_anchor.addClass('active');
          }

          // change href for li
           data_anchor.each(function() {
              if (!$(this).hasClass('active')){
                var tmp_href = $(this).attr('href');
                $(this).siblings('ul').find('a.left-md-anchor').attr('href', tmp_href);
              }
           });
        }
      }
      else if(q_l1.length > 0) {
          // parent li set expanded
          $("[href*='?l1=" + q_l1 +"']")
            .addClass('active')
            .parent().children('ul').show();
      }
      else if(q_l2.length > 0){
          // parent li set expanded
          $("[href*='?l2=" + q_l2 +"']")
          .addClass('active')
          .closest('ul').show();
        }
    }

    function alter_print_path(vocab_id) {
      //print pdf
      if ($('div.sbir_top_print_bar a.pdfPage').length > 0) {
        var old_pdf_url = $('div.sbir_top_print_bar a.pdfPage').attr('href');
        $('div.sbir_top_print_bar a.pdfPage').attr('href' /* ,  old_pdf_url +'&vocab='  + vocab_id */ );
      }

      //print
      if ($('div.sbir_top_print_bar a.printPage').length > 0) {
        var old_print_url = $('div.sbir_top_print_bar a.printPage').attr('href');
        $('div.sbir_top_print_bar a.printPage').attr('href' /* ,  old_print_url + '&vocab='  + vocab_id */ );
      }
    }

    // Source: http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values
    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }

    function scrollTopicOnLoad(){
      if (getParameterByName('topic') == ''){
        return;
      }
      divId = '#' + getParameterByName('topic');
      if($(divId).length > 0){
        $(divId).closest('li.md-taxonomy').children('div.taxonomyTopic').children('a.expandable-list').trigger('click');
        $('html, body').animate({
          scrollTop: $(divId).offset().top-100
        }, 500);

        var url = window.location.href;
        if (url.indexOf("&topic") > 0) {
            var updatedUri = url.substring(0, url.indexOf("&topic"));
            window.history.replaceState({}, document.title, updatedUri);
        }
        return;
      }
    }
    
  });

  $(document).ajaxComplete(function(event){

  });

})(jQuery);


