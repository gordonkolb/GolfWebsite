<?php
    function get_data() {

        $connect = mysqli_connect("localhost", "root", "joepettit", "foo");

        $query = "SELECT name FROM people";
        $result = mysqli_query ($connect, $query);
        $person_data = array();
        while($row = mysqli_fetch_array($result)) {
            $person_data[] = array(
                'name' => $row["name"]
            );
        }
        return json_encode($person_data);

    }

    echo '<pre>';
    print_r(get_data());
    echo '</pre>'
?>