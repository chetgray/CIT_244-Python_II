% rebase('_layout.tpl', page_title='Payroll', page_heading='Edit Employee Data')
<form action="/edit-employee-data" method="post">
    <div class="mb-3 col-sm-6">
        <label class="form-label" for="emp_id">Employee ID</label>
        <input class="form-control" id="emp_id" name="emp_id" type="number" required />
    </div>
    <div class="mb-3 col-sm-6">
        <label class="form-label" for="hrs_worked">Hours Worked</label>
        <input
            class="form-control"
            id="hrs_worked"
            name="hrs_worked"
            type="number"
            step="0.0001"
            min="0.0000"
            required
        />
    </div>
    <button class="btn btn-primary" type="submit">Update</button>
</form>
% if defined('alert_message'):
<div
    class="alert alert-{{ alert_context }} alert-dismissible fade show col-sm-6 my-3 px-3"
    role="alert"
>
    {{ alert_message }}
    <button class="btn-close" data-bs-dismiss="alert" type="button" aria-label="Close"></button>
</div>
% end
% end
