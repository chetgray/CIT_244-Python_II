% rebase('_layout.tpl', page_title='Payroll', page_heading='View Payroll by Department')
<form action="/view-by-department" method="post">
    <div class="mb-3 col-sm-6">
        <label class="form-label" for="department">Department</label>
        <select class="form-select" id="department" name="department">
            <option value="" selected>— All —</option>
            % for department in departments:
            <option value="{{ department }}">{{ department }}</option>
            % end
        </select>
    </div>
    <button class="btn btn-primary" type="submit">View</button>
    % end
</form>
