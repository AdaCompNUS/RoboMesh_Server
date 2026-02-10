#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point32
import time
import random

class FakeAgent(Node):
    def __init__(self):
        # Initialize ROS2 node
        super().__init__('fake_agent')
        
        # Publisher for robot feedback
        self.feedback_pub = self.create_publisher(String, '/robot_feedback', 10)
        
        # Subscribers for user input
        self.user_instruction_sub = self.create_subscription(
            String,
            '/user_instruction',
            self.user_instruction_callback,
            10
        )
        
        self.user_point_sub = self.create_subscription(
            Point32,
            '/user_point',
            self.user_point_callback,
            10
        )
        
        # Fake agent responses
        self.responses = [
            "I understand. Let me process that request.",
            "Got it! I'll help you with that.",
            "Processing your instruction now.",
            "Understood. Working on it.",
            "I've received your message and will act accordingly.",
            "Acknowledged. Let me handle that for you.",
            "Sure thing! I'm on it.",
            "No problem. I'll take care of that.",
        ]
        
        self.point_responses = [
            "I see you're pointing at coordinates ({:.3f}, {:.3f}).",
            "Noted the point at ({:.3f}, {:.3f}).",
            "Point received: ({:.3f}, {:.3f}).",
            "I've registered the point ({:.3f}, {:.3f}).",
        ]
        
        self.get_logger().info("Fake Agent initialized and ready")
        self.get_logger().info("Listening for user instructions and points...")

    def user_instruction_callback(self, msg):
        """Callback for user instruction messages"""
        user_input = msg.data
        self.get_logger().info(f"Received user instruction: {user_input}")
        
        # Simulate processing delay
        time.sleep(0.5)
        
        # Generate fake response
        response = random.choice(self.responses)
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            response = "Hello! How can I assist you today?"
        elif "help" in user_input.lower():
            response = "I'm here to help! What would you like me to do?"
        elif "move" in user_input.lower() or "go" in user_input.lower():
            response = "I'll move to the requested location."
        elif "stop" in user_input.lower():
            response = "Stopping all actions now."
        elif "?" in user_input or "what" in user_input.lower():
            response = "That's an interesting question. Let me think about that."

        # Publish feedback
        feedback_msg = String()
        feedback_msg.data = response
        self.feedback_pub.publish(feedback_msg)
        self.task_end()
        self.get_logger().info(f"Published feedback: {response}")

    def user_point_callback(self, msg):
        """Callback for user point messages"""
        x = msg.x
        y = msg.y
        self.get_logger().info(f"Received user point: x={x:.3f}, y={y:.3f}")
        
        # Simulate processing delay
        time.sleep(0.2)
        
        # Generate fake response
        response = random.choice(self.point_responses).format(x, y)
        
        # Publish feedback
        feedback_msg = String()
        feedback_msg.data = response
        self.feedback_pub.publish(feedback_msg)
        self.get_logger().info(f"Published feedback: {response}")

    def task_end(self):
        feedback_msg = String()
        feedback_msg.data = 'end'
        self.feedback_pub.publish(feedback_msg)

def main(args=None):
    rclpy.init(args=args)
    
    fake_agent = FakeAgent()
    
    try:
        rclpy.spin(fake_agent)
    except KeyboardInterrupt:
        fake_agent.get_logger().info("Shutting down Fake Agent...")
    finally:
        fake_agent.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

