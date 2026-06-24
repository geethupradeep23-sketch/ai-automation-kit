import json
from datetime import datetime
from typing import Dict, List, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Automate business workflows and processes"""
    
    def __init__(self):
        self.workflows = {}
        self.tasks = []
        self.triggers = {}
    
    def create_workflow(self, workflow_id: str, name: str, steps: List[Dict]):
        """
        Create a new workflow
        
        Args:
            workflow_id: Unique workflow ID
            name: Workflow name
            steps: List of workflow steps
        """
        workflow = {
            'id': workflow_id,
            'name': name,
            'steps': steps,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        self.workflows[workflow_id] = workflow
        logger.info(f"Workflow created: {name}")
        return workflow
    
    def execute_workflow(self, workflow_id: str, context: Dict):
        """
        Execute a workflow
        
        Args:
            workflow_id: ID of workflow to execute
            context: Context data for workflow
        
        Returns:
            Execution results
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow not found: {workflow_id}")
            return None
        
        workflow = self.workflows[workflow_id]
        results = []
        
        for step in workflow['steps']:
            logger.info(f"Executing step: {step.get('name')}")
            result = self._execute_step(step, context)
            results.append(result)
        
        logger.info(f"Workflow {workflow_id} completed")
        return results
    
    def _execute_step(self, step: Dict, context: Dict):
        """
        Execute a single workflow step
        """
        step_type = step.get('type')
        
        if step_type == 'create_task':
            return self._create_task(step, context)
        elif step_type == 'send_email':
            return self._send_email(step, context)
        elif step_type == 'update_crm':
            return self._update_crm(step, context)
        elif step_type == 'conditional':
            return self._conditional_step(step, context)
        
        return {'status': 'unknown'}
    
    def _create_task(self, step: Dict, context: Dict):
        """Create a task"""
        task = {
            'title': step.get('title', 'Untitled'),
            'description': step.get('description', ''),
            'assigned_to': step.get('assigned_to', ''),
            'due_date': step.get('due_date', ''),
            'status': 'open',
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        logger.info(f"Task created: {task['title']}")
        return {'status': 'success', 'task': task}
    
    def _send_email(self, step: Dict, context: Dict):
        """Send automated email"""
        email = {
            'to': step.get('to', ''),
            'subject': step.get('subject', ''),
            'body': step.get('body', ''),
            'timestamp': datetime.now().isoformat()
        }
        logger.info(f"Email sent to {email['to']}")
        return {'status': 'sent', 'email': email}
    
    def _update_crm(self, step: Dict, context: Dict):
        """Update CRM record"""
        logger.info("CRM record updated")
        return {'status': 'updated'}
    
    def _conditional_step(self, step: Dict, context: Dict):
        """Execute conditional step"""
        condition = step.get('condition')
        if_true = step.get('if_true')
        if_false = step.get('if_false')
        
        logger.info(f"Evaluating condition: {condition}")
        return {'status': 'evaluated'}
    
    def create_trigger(self, trigger_id: str, event: str, action: str):
        """
        Create an automated trigger
        
        Args:
            trigger_id: Unique trigger ID
            event: Event that triggers the action
            action: Action to perform
        """
        trigger = {
            'id': trigger_id,
            'event': event,
            'action': action,
            'created_at': datetime.now().isoformat()
        }
        self.triggers[trigger_id] = trigger
        logger.info(f"Trigger created: {event} -> {action}")
        return trigger
    
    def list_tasks(self, status=None):
        """
        List all tasks or filtered by status
        """
        if status:
            return [t for t in self.tasks if t['status'] == status]
        return self.tasks
    
    def update_task(self, task_index: int, updates: Dict):
        """
        Update a task
        """
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].update(updates)
            logger.info(f"Task updated at index {task_index}")
            return self.tasks[task_index]
        return None


if __name__ == "__main__":
    engine = WorkflowEngine()
    
    # Example: Create a workflow
    workflow = engine.create_workflow(
        'wf_001',
        'New Lead Follow-up',
        [
            {
                'type': 'create_task',
                'name': 'Create follow-up task',
                'title': 'Follow up with new lead',
                'assigned_to': 'sales_team'
            },
            {
                'type': 'send_email',
                'name': 'Send email',
                'to': 'lead@example.com',
                'subject': 'Welcome to our platform',
                'body': 'Thank you for your interest...'
            }
        ]
    )
    
    # Execute workflow
    results = engine.execute_workflow('wf_001', {})
    print(json.dumps(results, indent=2))
