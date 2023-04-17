% rebase("_layout.tpl", page_title=page_title, page_heading=page_heading)

<div class="table-responsive">
    <table class="table table-hover table-striped">
        <thead>
            <tr>
                <th scope="col">Trip ID</th>
                <th scope="col">Username</th>
                <th scope="col">Date</th>
                <th scope="col">Destination</th>
                <th scope="col">Miles</th>
                <th scope="col">Gallons</th>
                <th scope="col">MPG</th>
            </tr>
        </thead>
        <tbody>
            % for trip in trips:
            <tr>
                <td>{{ trip["trip_id"] }}</td>
                <td>{{ trip["username"] }}</td>
                <td>{{ trip["date"] }}</td>
                <td>{{ trip["destination"] }}</td>
                <td>{{ trip["miles"] }}</td>
                <td>{{ trip["gallons"] }}</td>
                <td>{{ f"{trip['mpg']:.1f}" if trip['mpg'] is not None else "" }}</td>
            </tr>
            % end
        </tbody>
    </table>
</div>
