import React from 'react';
import {Chart, ArcElement} from 'chart.js'
import {Pie, Doughnut} from 'react-chartjs-2';
Chart.register(ArcElement);

const state = {
  labels: ['January', 'February', 'March',
           'April', 'May'],
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
      data: [65, 59, 80, 81, 56]
    }
  ]
}

const PieChart =()=>{
  return(
    <div style={{height:'20vw', width:'20vw'}}>
      <Pie
          data={state}
          options={{
            title:{
              display:true,
              text:'Average Rainfall per month',
              fontSize:20
            },
            legend:{
              display:true,
              position:'top'
            }
          }}
          height={20}
          width={40}
        />
    </div>
  )
}

export default PieChart