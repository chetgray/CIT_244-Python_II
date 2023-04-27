% rebase('_layout.tpl', page_title='Payroll', page_heading='Edit Employee Data')
<form action="/edit-employee-data" method="post">
    <div class="mb-3 col-sm-6">
        <label class="form-label" for="emp_id">Employee ID</label>
        <input class="form-control" id="emp_id" name="emp_id" type="number" required>
    </div>
    <div class="mb-3 col-sm-6">
        <label class="form-label" for="hrs_worked">Hours Worked</label>
        <input class="form-control" id="hrs_worked" name="hrs_worked" type="number" required>
    </div>
    <button class="btn btn-primary" type="submit">Update</button>
</form>
% end
