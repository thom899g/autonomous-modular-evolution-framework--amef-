import logging
from typing import Dict, Any
from modules.learning_module import LearningModule
from modules.feedback_loop import FeedbackLoop
from modules.configuration_manager import ConfigurationManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MasterAgent:
    """The central controller of the AMEF ecosystem, managing module evolution and feedback loops.
    
    Attributes:
        modules: Dictionary of registered AI modules.
        learning_module: Instance of LearningModule for reinforcement learning.
        feedback_loop: Instance of FeedbackLoop for processing environmental feedback.
        config_manager: Instance of ConfigurationManager for handling configurations.
    """
    
    def __init__(self):
        self.modules = {}
        self.learning_module = LearningModule()
        self.feedback_loop = FeedbackLoop()
        self.config_manager = ConfigurationManager()
        
        # Initialize logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    def register_module(self, name: str, module_class) -> None:
        """Register a new AI module into the ecosystem."""
        try:
            self.modules[name] = module_class()
            logger.info(f"Module '{name}' registered successfully.")
        except Exception as e:
            logger.error(f"Failed to register module '{name}': {str(e)}")
            raise
    
    def deregister_module(self, name: str) -> None:
        """Deregister an AI module from the ecosystem."""
        if name in self.modules:
            del self.modules[name]
            logger.info(f"Module '{name}' deregistered successfully.")
        else:
            logger.warning(f"Module '{name}' not found.")
    
    def process_feedback(self, feedback: Dict[str, Any]) -> None:
        """Process feedback from the environment and update modules."""
        try:
            # Use feedback loop to generate meaningful insights
            insights = self.feedback_loop.analyze(feedback)
            
            # Update learning module with new insights
            self.learning_module.update_policy(insights)
            
            # Propagate feedback to relevant modules
            for module in self.modules.values():
                if hasattr(module, 'receive_feedback'):
                    module.receive_feedback(insights)
                    
        except Exception as e:
            logger.error(f"Failed to process feedback: {str(e)}")
            raise
    
    def run_cycle(self) -> None:
        """Execute a full cycle of the ecosystem's operations."""
        try:
            # Update configurations
            self.config_manager.apply_config()
            
            # Run all registered modules
            for name, module in self.modules.items():
                logger.info(f"Running module '{name}'...")
                module.run()
                
            # Collect and process feedback
            feedback = self.feedback_loop.collect_feedback(self.modules)
            self.process_feedback(feedback)
            
        except Exception as e:
            logger.error(f"Failed to run cycle: {str(e)}")
            raise