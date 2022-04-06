import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';

// Delete after test
const columns = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'firstName', headerName: 'First name', width: 130 },
  { field: 'lastName', headerName: 'Last name', width: 130 },
  {
    field: 'age',
    headerName: 'Age',
    type: 'number',
    width: 90,
  },
  {
    field: 'fullName',
    headerName: 'Full name',
    description: 'This column has a value getter and is not sortable.',
    sortable: false,
    width: 160,
    valueGetter: (params) =>
      `${params.row.firstName || ''} ${params.row.lastName || ''}`,
  },
];

// Delete after test
const rows = [
  { id: 1, lastName: 'Snow', firstName: 'Jon', age: 35 },
  { id: 2, lastName: 'Lannister', firstName: 'Cersei', age: 42 },
  { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 45 },
  { id: 4, lastName: 'Stark', firstName: 'Arya', age: 16 },
  { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null },
  { id: 6, lastName: 'Melisandre', firstName: null, age: 150 },
  { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44 },
  { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36 },
  { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65 },
];

function DataTable(props) {

  // console.log(props);

  const choice_array = props.question.question.choices;
  const data_columns = choice_array.map((name) => {
    let obj = {};
    obj['field'] = name.id;
    obj['headerName'] = name.description;
    obj['width'] = 130;
    return obj;
  });
  let breakoutRoom = [{ field: 'breakoutRoom', headerName: 'Breakout Room', width: 130 }];
  let real_columns = breakoutRoom.concat(data_columns);
  /* If there is no breakout room, no need to create a separate column */
  if (props.groups.length === 0) {
    real_columns = data_columns;
  }

  // console.log(column_name_object);

  const data_byGroup = props.question.by_group;
  const sortGroup_array = props.groups;
  // console.log(data_byGroup);
  let real_data = [];
  /* If there is no breakout room */
  if (sortGroup_array.length === 0) {
    let obj = {};
    obj['id'] = 0;
    choice_array.map((choice, index) => {
      const choice_id = choice.id;
      const cell_data = props['question']['all']['ranking'][choice_id]['mean'];
      obj[choice_id] = cell_data;
    });
    real_data.push(obj);
  }
  /* If there are several breakout rooms */
  else {
    const data_rows = sortGroup_array.map((group, index) => {
      let obj = {};
      obj['id'] = index;
      obj['breakoutRoom'] = group.description;
      const group_id = group.id;
      const temp = choice_array.map((choice) => {
        const choice_id = choice.id;
        //Display the mean value by default
        const cell_data = data_byGroup[group_id]['ranking'][choice_id]['mean'];
        obj[choice_id] = cell_data;
      });
      return obj;
    });
    real_data = data_rows;
  }

  // console.log(data_rows);


  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={real_data}
        columns={real_columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />
    </div>
  );
}

export default DataTable