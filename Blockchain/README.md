**Install and activate the virtual env**
python -m venv blockchain-env
```blockchain-env/scripts/activate```
**To install packages and module**
```Pyhton -m -r requirement.txt```
**Run Pytest**
Make sure to activate the virtual env
```python -m pytest backend.util.tests```

**Run the application and API**
Make sure to activate the virtual env
```python3 -m backend.app```
**Run the Peer Instance**
Make sure to activate the virtaul environment
```export PEER=True && python3 -m backend.app ```
for windows
```$env:PEER = 'True'; python -m backend.app```

<!-- subscribe_key='sub-c-4ab2851d-6334-46ca-86f9-157b1c2efd53 -->
<!-- pub-c-68ee9821-af71-4613-90af-39f8c4442ac2 -->

**If the moduel is not found or no module error you can use this module**

```import sys
    sys.path.append('.')```
