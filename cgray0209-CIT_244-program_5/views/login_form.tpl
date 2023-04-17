% rebase('_layout.tpl', page_title='Login', page_heading='Login')
<form action="/" method="post">
    <input name="action" type="hidden" value="login">
    <div>
        <label for="username">Email:</label>
        <input id="username" name="username" type="text">
    </div>
    <div>
        <label for="password">Password:</label>
        <input id="password" name="password" type="password">
    </div>
    <div>
        <input type="submit" value="Login">
    </div>
</form>
