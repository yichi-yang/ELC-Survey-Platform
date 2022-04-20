import React from 'react';
import {Chart, ArcElement, Legend, Tooltip} from 'chart.js'
import {Pie} from 'react-chartjs-2';
Chart.register(ArcElement);
Chart.register(Legend);
Chart.register(Tooltip);

function PieChart(props){

  const labels = [];
  const data=[];

  Object.entries(props.index===0?props.question.all.count:props.question.by_group[props.index].count).forEach(([key, value]) => {
    data.push(value);
  })

  Object.entries(props.question.question.choices).forEach((key, value) => {
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

  let deter = 0;
  data.forEach(number=>{
    if(number!==0){
      deter=1;
    }
  })
  return(
    deter===1?
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
    :<div style={{height:'5vw', width:'25vw'}}>
    No Submission
  </div>
  )
}

export default PieChart