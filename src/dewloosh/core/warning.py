"""
Warnings used in DewLoosh projects.
"""

class PerformanceWarning(Warning):
    
    def __init__(self, message: str):
        pre = "DewLoosh Performance Warning: "
        self.message = pre + message