% rebase('_layout.tpl', page_title='Payroll', page_heading='View Payroll')
% if defined('alert_message'):
<div
    class="alert alert-{{ alert_context }} alert-dismissible fade show col-sm-6 my-3 px-3"
    role="alert"
>
    {{ alert_message }}
    <button class="btn-close" data-bs-dismiss="alert" type="button" aria-label="Close"></button>
</div>
% end
<dl class="row">
    <dt class="col-2">Department</dt>
    <dd class="col-10">{{ department if department else 'All' }}</dd>
    <dt class="col-2">Pay Period</dt>
    <dd class="col-10">{{ pay_period }}</dd>
</dl>
% if not employees:
<div class="alert alert-warning col-sm-6 my-3 px-3" role="alert">
    No records found.
</div>
% else:
<div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
        <thead>
            <tr>
                <th scope="col">Employee ID</th>
                <th scope="col">Name</th>
                <th scope="col">Department</th>
                <th scope="col">Hours Worked</th>
                <th scope="col">Hourly Rate</th>
                <th scope="col">Gross Pay</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            % for employee in employees:
            <tr>
                <th scope="row">{{ employee.emp_id }}</th>
                <td>{{ employee.emp_name }}</td>
                <td>{{ employee.department }}</td>
                <td>{{ employee.hrs_worked }}</td>
                <td>{{ f"$ {employee.wage:,.2f}" }}</td>
                <td>{{ f"$ {employee.gross_pay:,.2f}" }}</td>
            </tr>
            % end
        </tbody>
    </table>
</div>
% end
% end
