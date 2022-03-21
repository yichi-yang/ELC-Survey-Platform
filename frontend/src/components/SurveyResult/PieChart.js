import React from 'react';
import {Chart, ArcElement, Legend, Tooltip} from 'chart.js'
import {Pie, Doughnut} from 'react-chartjs-2';
Chart.register(ArcElement);
Chart.register(Legend);
Chart.register(Tooltip);

function PieChart(props){

  console.log(props.question.question.choices)

  const labels = [];
  const data=[];

  Object.entries(props.question.all.count).map(([key, value]) => {
    data.push(value);
  })

  Object.entries(props.question.question.choices).map((key, value) => {
    labels.push(key[1].description)
  })

  const state = {
    labels: labels,
    datasets: [
      {
        label: 'multiple',
        backgroundColor: [
          '#B21F00',
          '#C9DE00',
          '#2FDE00',
          '#00A6B4',
          '#6800B4'
        ],
        hoverBackgroundColor: [
        '#501800',
        '#4B5000',
        '#175000',
        '#003350',
        '#35014F'
        ],
        data: data
      }
    ]
  }  

  return(
    <div style={{height:'25vw', width:'25vw'}}>
      <Pie
          data={state}
          options={{
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'right',
              },
              title: {
                display: true,
                text: 'Chart.js Pie Chart'
              }
            },
            
          }}
          height={25}
          width={25}
        />
    </div>
  )
}

export default PieChart