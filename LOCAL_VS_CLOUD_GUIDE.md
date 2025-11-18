# Streamlit: Local vs Cloud Deployment Guide

## Key Lessons Learned

### 1. **Data Files Must Be in GitHub Repo**

**Problem:** App worked locally but failed on Streamlit Cloud with "NoneType" errors.

**Cause:** Data files were in local directory but not pushed to GitHub.

**Solution:**
```bash
# Make sure all data files are tracked and pushed
git add data/
git commit -m "Add data files"
git push origin main
```

✅ **Always verify:** Check your GitHub repo in the browser - all data files should be visible.

---

### 2. **API Responses Differ Between Environments**

**Problem:** API calls work locally but return `None` or different structures on cloud.

**Cause:** Network conditions, API rate limits, or response formats differ.

**Solution:** Always validate API responses before using them:

```python
# ❌ BAD - Will crash if response is None
result = api_call()
data = result['key']

# ✅ GOOD - Safe validation
result = api_call()
if result is None:
    return {'error': 'API returned None'}
if 'key' not in result:
    return {'error': 'Missing expected key'}
data = result.get('key', 'default')
```

---

### 3. **Environment Variables / Secrets**

**Local:**
```python
# Uses .env file
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

**Cloud:**
```python
# Uses Streamlit secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv('GEMINI_API_KEY')  # Fallback for local
```

**Setup Cloud Secrets:**
1. Go to app settings on share.streamlit.io
2. Click "Secrets"
3. Add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```

---

### 4. **File I/O Permissions**

**Problem:** Code writes logs locally but fails silently on cloud.

**Cause:** Streamlit Cloud has limited write permissions.

**Solution:** Wrap all file operations in try-except:

```python
# ✅ Safe file writing
try:
    with open('log.txt', 'w') as f:
        f.write(data)
except Exception as e:
    print(f"Warning: Could not save log: {e}")
    # Continue execution - don't crash
```

**Tip:** Only write to temporary directories or make logging optional.

---

### 5. **Error Handling Best Practices**

Always use safe dictionary access:

```python
# ❌ BAD
value = dict['key']

# ✅ GOOD  
value = dict.get('key', 'default_value')
```

Wrap critical operations:

```python
try:
    result = critical_operation()
    if result is None:
        return handle_error()
    return process_result(result)
except Exception as e:
    return {'error': str(e)}
```

---

### 6. **Repository Structure**

**Must be flat and include everything:**

```
project/
├── streamlit_app.py          # Main app file
├── module1.py                # Your modules
├── module2.py
├── requirements.txt          # ALL dependencies
├── data/                     # Data files (if not too large)
│   ├── file1.csv
│   └── file2.xlsx
├── .gitignore               # Don't ignore data/
└── README.md
```

**Don't use nested packages** unless absolutely necessary - Streamlit Cloud prefers flat structure.

---

### 7. **Testing Checklist**

Before deploying:

- [ ] All data files pushed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] API responses validated before use
- [ ] Dictionary access uses `.get()` method
- [ ] File I/O wrapped in try-except
- [ ] Secrets configured on Streamlit Cloud
- [ ] Test locally with `streamlit run app.py`
- [ ] Check GitHub repo has all files

---

### 8. **Common Errors & Fixes**

| Error | Cause | Fix |
|-------|-------|-----|
| `NoneType object is not subscriptable` | API returned None, tried to access keys | Add response validation |
| `FileNotFoundError` | Data files not in GitHub | Push data files to repo |
| `KeyError` on secrets | Forgot to set secrets on cloud | Add secrets in Streamlit Cloud settings |
| `Module not found` | Missing from requirements.txt | Add to requirements.txt |
| Works locally, fails on cloud | Environment differences | Add error handling & validation |

---

### 9. **Deployment Workflow**

```bash
# 1. Test locally
streamlit run streamlit_app.py

# 2. Commit changes
git add .
git commit -m "Your message"

# 3. Push to GitHub
git push origin main

# 4. On Streamlit Cloud:
#    - App auto-deploys
#    - Check secrets are set
#    - Monitor logs for errors

# 5. If errors occur:
#    - Check Streamlit Cloud logs
#    - Verify all files in GitHub repo
#    - Check secrets configuration
```

---

## Quick Debug Guide

**App crashes on Streamlit Cloud but works locally?**

1. ✅ Check if data files are in GitHub repo
2. ✅ Verify secrets are configured on cloud
3. ✅ Look for file I/O operations (may need try-except)
4. ✅ Check API calls have response validation
5. ✅ Review Streamlit Cloud logs for actual error

**NoneType errors?**

- API response validation missing
- Dictionary accessed without `.get()`
- Data files not loaded (check GitHub)

---

## Summary

**The Golden Rule:** If it works locally but fails on cloud, the issue is usually:
1. Missing files in GitHub (data, config)
2. Missing/incorrect secrets configuration  
3. API responses not validated
4. File I/O without error handling

**Always validate everything before accessing it!**

