
var elButton = document.getElementById('update');
var elInput = document.getElementById('number');
var elInfo = document.getElementById('info');
var elTable = document.getElementById('rooster');

elButton.addEventListener('click', function(event) {
  var value = parseInt(elInput.value);
  setEmptyTable();
  doRequest(value);
});

setEmptyTable = function() {
  elTable.innerHTML = '<tr><th></th><th>maandag</th><th>dinsdag</th><th>woensdag</th><th>donderdag</th><th>vrijdag</th></tr>';
  for (var q = 0; q < 9; q++) {
    var elTr = document.createElement('tr');
    elTr.innerHTML = '<td><strong>'+q+'</strong></td>';
    for (var p = 0; p < 5; p++) {
      elTr.innerHTML += '<td data-hour='+q+' data-day='+p+'></td>'
    }
    elTable.appendChild(elTr);
  }
}

doRequest = function(number) {
  var request = new XMLHttpRequest();
  request.open('GET', '/rooster-'+number+'.json', true);

  request.onload = function() {
    if (this.status >= 200 && this.status < 400) {
      var data = JSON.parse(this.response);
      json2table(data);
    } else {
      alert("Error getting json. Does the file rooster-"+number+".json exist?");
    }
  };

  request.onerror = function() {
    alert("Connection error, check your internet.");
  };

  request.send();
}

json2table = function(json) {
  //console.log(json);

  var name = json.name;
  var date = json.date;
  var week = json.week;
  var rooster = json.rooster;

  elInfo.querySelectorAll('#name')[0].innerHTML = '<strong>Naam</strong> '+name+'<br>';
  elInfo.querySelectorAll('#date')[0].innerHTML = '<strong>Datum uitgifte</strong> '+date+'<br>';
  elInfo.querySelectorAll('#week')[0].innerHTML = '<strong>Weeknummer</strong> '+week+'<br>';

  roosterSorted = {};
  for (var i in rooster) {

    var appointment = rooster[i];
    var day = appointment.day;
    var hour = appointment.hour;

    if (!roosterSorted[hour]) {
      roosterSorted[hour] = {};
    }

    roosterSorted[hour][day] = appointment;
    continue;

  }
  //console.log(roosterSorted);
  for (var i in roosterSorted) {
    var hours = roosterSorted[i];

    for (var n in hours) {
      var hour = hours[n];
      //console.log(hour);
      elTable.querySelectorAll('[data-day="'+hour.day+'"][data-hour="'+hour.hour+'"]')[0].innerHTML = hour.subject+'<br>Lokaal '+hour.classroom;
    }

  }

}
