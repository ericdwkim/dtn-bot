from src.app.flow_manager import FlowManager
def first_flow():
    flow_manager = FlowManager()

    try:
        flow_manager.start_flow()
        # first flow specific logic
    finally:
        flow_manager.end_flow()


first_flow()

# def second_flow():
#     flow_manager = FlowManager()
#
#     try:
#         flow_manager.start_flow()
#         # ... Rest of second_flow logic ...
#     finally:
#         flow_manager.end_flow()
#
#
#
# def third_flow():
#
#     # third flow specific logic
#     pass
#
#
#
# def run_flows():
#     # first , second, third flows execution wrapper for sequential runs
#     pass
#
