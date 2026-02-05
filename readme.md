# Cash Flow Statement Calculator

First attempt to some kind of vibe-code on new platform.

This is a simple cash flow statement calculator written in Python. It can calculate the following indicators:
- Operational Cash Flow
- Investing Cash Flow
- Financing Cash Flow
- Cash

## Troubleshooting

### ModuleNotFoundError: No module named 'cash_flow_engine'
If you see this error when running the notebook, it means your Jupyter Kernel is running in a different directory. To fix this:
1. Ensure you opened the workspace or notebook from the `Cash Flow Statement` directory.
2. Or, add the following code to the top of your notebook:
   ```python
   import sys
   import os
   if os.getcwd() not in sys.path:
       sys.path.append(os.getcwd())
   ```