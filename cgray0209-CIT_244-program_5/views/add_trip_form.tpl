% rebase("_layout.tpl", page_title="Add a Trip", page_heading="Add a Trip")
<form action="/add" method="post">
    <div>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" />
    </div>
    <div>
        <label for="date">Date</label>
        <input id="date" name="date" type="date" />
    </div>
    <div>
        <label for="destination">Destination</label>
        <input id="destination" name="destination" type="text" />
    </div>
    <div>
        <label for="miles">Total Miles</label>
        <input id="miles" name="miles" type="number" />
    </div>
    <div>
        <label for="gallons">Total Gallons</label>
        <input id="gallons" name="gallons" type="number" />
    </div>
    <div>
        <button class="btn btn-primary" type="submit">Submit</button>
    </div>
</form>
% if defined('alert_message'):
<p class="alert alert-{{ alert_context }}" role="alert">{{ alert_message }}</p>
% end
