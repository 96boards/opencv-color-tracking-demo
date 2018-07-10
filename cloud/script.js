// Our labels along the x-axis
var colors = ["Red","Yellow","Black","Blue","Green","Orange"];

// For drawing the lines
var red=5;
var yellow=6;
var black=7;
var blue=2;
var green=9;
var orange=10;


var ctx = document.getElementById("myChart");

var dts =  [
      {
        label: "Current count",
        backgroundColor: ["#FF0000", "#F7FF00","#000000","#0000FF","#00FF00","#F87000"],
        data: [red,yellow,black,blue,green,orange],
      }
     ]

var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: colors,
    datasets: dts
    },
    options: {
        legend: {display: false},
        title: {
            display: true,
            text: 'Count'
        },
        scales: {
            yAxes: [{
            ticks: {
                beginAtZero: true
            }
          }]
        }
    }
  });

// Update Chart every 2 seconds with latest color data
setInterval(function(){
  myChart.data.datasets[0].data[0]=red
  myChart.data.datasets[0].data[1]=yellow
  myChart.data.datasets[0].data[2]=black
  myChart.data.datasets[0].data[3]=blue
  myChart.data.datasets[0].data[4]=green
  myChart.data.datasets[0].data[5]=orange
  //myChart.data.labels[1] = "New One";
  myChart.update();
},2000);

// STUB  -  Update Color data.  May be read from a local file or filled in with Cloud located data.
setInterval(function(){
  red=red+1;
  yellow=yellow+1;
  black=black+1;
  blue=blue+1;
  green=green+1;
  orange=orange+1;
},4000);

