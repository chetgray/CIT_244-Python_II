% rebase('_layout.tpl', page_title='Login', page_heading='Login')
<form action="/" method="post">
    <div>
        <label for="username">Email:</label>
        <input id="username" name="username" type="text" />
    </div>
    <div>
        <label for="password">Password:</label>
        <input id="password" name="password" type="password" />
    </div>
    <div>
        <input type="submit" value="Login" />
    </div>
</form>
% if defined('alert_message'):
<p class="alert alert-{{ alert_context }}" role="alert">{{ alert_message }}</p>
% end
