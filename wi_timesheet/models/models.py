from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime , time
from pytz import timezone, UTC
import pytz

class ProjectTaskTimeSheet(models.Model):
    _inherit = 'account.analytic.line'

    date_start = fields.Datetime(string='Start Date', default=False)
    date_end = fields.Datetime(string='End Date', default=False)
    task_state = fields.Selection(compute="_compute_state", string="Status", selection=[('new','New'),('pending','On Going'),('done','Finished')])
    unit_amount = fields.Float()
    task_toggle = fields.Boolean(string="Trigger Activation" , default=False ,compute="_task_toggle")

    @api.onchange('date')
    def startend_date(self):
        date_compare = datetime.date(datetime.now())
        for assign_date in self:
            if assign_date.date != date_compare:
                date_year = assign_date.date.year
                date_month = assign_date.date.month
                date_days = assign_date.date.day
                assign_date.date_start = datetime(date_year,date_month,date_days-1, 17, 0, 0)
                assign_date.date_end = datetime(date_year,date_month,date_days-1, 17, 0, 0)
                
    def _compute_state(self):
        for task in self:
            if task.date_start and task.date_end :
                task.task_state = "done"
            elif task.date_end == False and task.date_start:
                task.task_state = "pending"
            elif task.unit_amount > 0 :
                task.task_state = "done"
            else:
                task.task_state = "new"
    
    @api.onchange("task_toggle","date_end","unit_amount","date_start")
    def _calc_time_taken(self):
        for time in self:
            if time.date_start and time.date_end:
                cal_date = time.date_end - time.date_start
                time.unit_amount = (cal_date.total_seconds()/3600.0)
                if time.unit_amount < 0 :
                    time.date_end = False
                    time.date_start = False
                
                elif time.unit_amount > 24.00:
                    time.date_end= False

            elif time.date_start and time.date_end == False:
                time.date_end == False 
                
            else:
                if time.unit_amount > 0 and time.unit_amount < 24 and time.date_start == False and time.date_start == False :
                    time.task_state = 'done'
                elif time.unit_amount > 24:
                    raise UserError("Duration Should not be bigger than 24 Hour")
                elif time.unit_amount <0 :
                    raise UserError("Duration can't be negative")
                elif time.date_start and time.unit_amount > 0 and time.date_end == False:
                    raise UserError("Remove date start to proceed input duration")
                else:
                    time.unit_amount = False
    
    @api.onchange("task_toggle")
    def _toggle_task(self):
        for toggle in self:   
            if toggle.task_toggle == False:
                if toggle.date_start == False:
                    toggle.date_end =False
                else:
                    toggle.date_end = datetime.now()
                    toggle._calc_time_taken()
                    # if toggle.date_end.date()!=toggle.date_start.date():
                    #     raise UserError("The end time date must be the same as the start time date")
                    
            elif toggle.task_toggle == False and toggle.date_start:
                toggle.task_toggle = True 
            else:
                if toggle.date_start == False:
                    toggle.date_start = datetime.now()
            
    @api.onchange("date_start")
    def _task_toggle (self):
        for toggle in self:
            if toggle.task_toggle== False and toggle.date_start:
                toggle.task_toggle = True 

            elif toggle.date_start ==False and toggle.date_end ==False:
                toggle.task_toggle = False
                    

    @api.onchange("date_end")
    def _validate_time (self):
        
        for time in self:
            if time.date_end and time.date_start == False:
                raise UserError('The start time must be filled first before the end time')
            
            elif time.date_end and time.date_start:
                if time.date_end < time.date_start:
                    raise UserError('End time should not be earlier than Start time')

                elif time.convert_datetime_field(time.date_start).date()!=time.convert_datetime_field(time.date_end).date() :
                    raise UserError("The end time date must be the same as the start time date")


    def convert_datetime_field(self,time):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        date_convert = pytz.utc.localize(time).astimezone(user_tz)
        return date_convert