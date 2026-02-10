#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point32
import time
import random

class FakeAgent:
    def __init__(self):
        # Publisher for robot feedback
        self.feedback_pub = rospy.Publisher('/robot_feedback', String, queue_size=10)
        
        # Subscribers for user input
        self.user_instruction_sub = rospy.Subscriber(
            '/user_instruction',
            String,
            self.user_instruction_callback
        )
        
        self.user_point_sub = rospy.Subscriber(
            '/user_point',
            Point32,
            self.user_point_callback
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
        
        rospy.loginfo("Fake Agent initialized and ready")
        rospy.loginfo("Listening for user instructions and points...")

    def user_instruction_callback(self, msg):
        """Callback for user instruction messages"""
        user_input = msg.data
        rospy.loginfo(f"Received user instruction: {user_input}")
        
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
        rospy.loginfo(f"Published feedback: {response}")

    def user_point_callback(self, msg):
        """Callback for user point messages"""
        x = msg.x
        y = msg.y
        rospy.loginfo(f"Received user point: x={x:.3f}, y={y:.3f}")
        
        # Simulate processing delay
        time.sleep(0.2)
        
        # Generate fake response
        response = random.choice(self.point_responses).format(x, y)
        
        # Publish feedback
        feedback_msg = String()
        feedback_msg.data = response
        self.feedback_pub.publish(feedback_msg)
        rospy.loginfo(f"Published feedback: {response}")

    def task_end(self):
        feedback_msg = String()
        feedback_msg.data = 'end'
        self.feedback_pub.publish(feedback_msg)

def main():
    rospy.init_node('fake_agent')
    
    fake_agent = FakeAgent()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down Fake Agent...")

if __name__ == "__main__":
    main()

