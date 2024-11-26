// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});


$(document).ready(function (){
      $.ajax({
      url: "/pie",
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {
        console.log(jsonResponse)
         const title = jsonResponse.title;
        const labels = jsonResponse.data.labels;
        const datasets = jsonResponse.data.datasets;
        // Reset the current chart
        myPieChart.data.datasets = [];
        myPieChart.data.labels = [];
        // Load new data into the chart
        myPieChart.options.title.text = title;
        myPieChart.options.title.display = true;
        myPieChart.data.labels = labels;
        datasets.forEach(dataset => {
          myPieChart.data.datasets.push(dataset);
        });
        myPieChart.update();
      },
       error: () => console.log("Failed to fetch chart filter options!")
     });
});

/*
,
  data: {
    labels: ["Direct", "Referral", "Social"],
    datasets: [{
      data: [55, 30, 15],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },*/
