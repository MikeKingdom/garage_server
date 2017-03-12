function show_state(data) {
   if (data) {
       if (typeof data === "string") {
           try {
               data = JSON.parse(data);
           }
           catch (e) {
           }
       }
       $('#state').text(data.state);
       $('#door-state-open').toggle(data.state === 'open');
       $('#door-state-middle').toggle(data.state === 'middle');
       $('#door-state-closed').toggle(data.state === 'closed');
       $('#temperature').text(data.temperature);
   }
}

function door_close() {
    $.ajax({
         url: '/rest/garage',
         type: 'POST',
         contentType: 'application/json',
         data: '{"state":"closed"}',
         dataType: 'json',
         success: function(data, status, xhr) {
             show_state(data);
         }
    });
}

function door_open() {

    $.ajax({
         url: '/rest/garage/open',
         type: 'GET',
         headers: { "Accept" : "application/json" },
         success: function(response, status, xhr) {
             show_state(response);
         }
    });
}

function update_state() {

    $.ajax({
         url: '/rest/garage',
         type: 'GET',
         headers: { "Accept" : "application/json" },
         success: function(response, status, xhr) {
             show_state(response);
         }
    });
}

function update_img() {
	$('#camera').attr('src', 'get_image?' + (new Date()).getTime());
}

$( document ).ready(function() {
    setInterval(update_state, 5000);
    update_img();
    setInterval(update_img, 20000);
});
