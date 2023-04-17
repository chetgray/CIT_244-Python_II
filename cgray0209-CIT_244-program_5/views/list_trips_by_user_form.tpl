% rebase("_layout.tpl", page_title="Trips by User", page_heading="Trips by User")
<form action="/listByUser" method="post">
    <div>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" />
    </div>
    <div>
        <button class="btn btn-primary" type="submit">Submit</button>
    </div>
</form>
% if defined('alert_message'):
<p class="alert alert-{{ alert_context }}" role="alert">{{ alert_message }}</p>
% end
