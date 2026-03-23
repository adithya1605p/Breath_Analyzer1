# VayuDrishti Action Plan - Next 4 Weeks

**Start Date:** March 24, 2026  
**End Date:** April 21, 2026  
**Goal:** Improve accuracy from 69.5% to 85%+ and fix critical issues

---

## 📅 Week-by-Week Breakdown

### Week 1: Critical Fixes & Data Collection

#### Monday-Tuesday (Days 1-2): Security & Setup
- [ ] **Security Hardening** (Priority: CRITICAL)
  - Rotate WAQI API token
  - Rotate Supabase credentials
  - Move secrets to Google Secret Manager
  - Remove service account files from repo
  - Update .gitignore
  - Create .env.template
  - **Owner:** DevOps
  - **Time:** 2 days

#### Wednesday-Friday (Days 3-5): Data Collection
- [ ] **Collect Training Data**
  - Run `collect_training_data.py` for 24 hours
  - Download OpenAQ historical data (365 days)
  - Collect Dwarka-specific data (30 days)
  - **Owner:** Data Engineer
  - **Time:** 3 days (mostly automated)
  - **Deliverable:** `training_data_raw.csv` (10,000+ records)

#### Weekend: Data Preprocessing
- [ ] **Preprocess Data**
  - Run `preprocess_training_data.py`
  - Handle missing values
  - Add temporal features
  - Add spatial features
  - **Owner:** Data Scientist
  - **Time:** 2 days
  - **Deliverable:** `training_data_processed.csv`

---

### Week 2: Model Training & API Fixes

#### Monday-Tuesday (Days 8-9): Feature Engineering
- [ ] **Create Features**
  - Run `create_features.py`
  - Engineer 20+ features
  - Create PM10/PM2.5 ratio features
  - Add construction zone indicators
  - **Owner:** Data Scientist
  - **Time:** 2 days
  - **Deliverable:** Feature matrix ready for training

#### Wednesday-Friday (Days 10-12): Model Training
- [ ] **Train Improved Model**
  - Implement `ImprovedAQIPredictor` architecture
  - Train for 100 epochs
  - Monitor validation loss
  - Save best model
  - **Owner:** ML Engineer
  - **Time:** 3 days
  - **Deliverable:** `improved_model_best.pt`, `improved_scaler.pkl`

#### Parallel Track: Fix API Endpoints
- [ ] **Fix Forecast Endpoint**
  - Debug response format issue
  - Update parsing logic
  - Test with multiple locations
  - **Time:** 1 day

- [ ] **Fix Navigation Endpoint**
  - Register route in API router
  - Test routing functionality
  - **Time:** 1 day

- [ ] **Optimize GEE Endpoint**
  - Add caching layer
  - Reduce timeout from 30s to 10s
  - **Time:** 1 day

---

### Week 3: Model Evaluation & Integration

#### Monday-Tuesday (Days 15-16): Model Evaluation
- [ ] **Evaluate Model Performance**
  - Run `evaluate_model.py`
  - Calculate MAE, RMSE, R² for PM2.5 and PM10
  - Generate prediction vs actual plots
  - Analyze error distribution
  - **Owner:** Data Scientist
  - **Time:** 2 days
  - **Target:** PM2.5 MAE < 15, PM10 MAE < 25

#### Wednesday-Thursday (Days 17-18): Model Integration
- [ ] **Integrate New Model**
  - Update `ml_engine.py` to `ml_engine_v2.py`
  - Add PM10 prediction support
  - Update AQI calculation logic
  - Add construction zone adjustments
  - **Owner:** Backend Developer
  - **Time:** 2 days

#### Friday (Day 19): Testing
- [ ] **Run Validation Tests**
  - Run `test_aqi_validation.py`
  - Compare with WAQI for 10 locations
  - Document accuracy improvements
  - **Target:** Average accuracy > 80%

---

### Week 4: Features & Deployment

#### Monday-Tuesday (Days 22-23): Confidence Intervals
- [ ] **Implement Uncertainty Quantification**
  - Add Monte Carlo dropout
  - Calculate confidence intervals
  - Update API responses
  - **Owner:** ML Engineer
  - **Time:** 2 days

#### Wednesday (Day 24): Multi-Source Integration
- [ ] **Add OpenAQ Integration**
  - Implement OpenAQ API client
  - Add weighted averaging
  - Test data quality
  - **Owner:** Backend Developer
  - **Time:** 1 day

#### Thursday (Day 25): Dwarka Validation
- [ ] **Validate Dwarka Improvements**
  - Test PM10 prediction in Dwarka
  - Verify construction zone handling
  - Compare with WAQI real-time data
  - **Target:** Dwarka accuracy < 20% difference

#### Friday (Day 26): Documentation & Deployment
- [ ] **Update Documentation**
  - Update API documentation
  - Create model card
  - Write deployment guide
  - **Time:** 0.5 day

- [ ] **Deploy to Production**
  - Deploy new model to backend
  - Update frontend to show PM10
  - Monitor for errors
  - **Time:** 0.5 day

---

## 📊 Success Metrics

### Accuracy Targets

| Metric | Current | Week 2 | Week 4 | Target |
|--------|---------|--------|--------|--------|
| Overall Accuracy | 69.5% | 75% | 85% | 85%+ |
| Central Delhi | 91.5% | 93% | 95% | 95%+ |
| Industrial Areas | 62% | 70% | 80% | 80%+ |
| Dwarka Accuracy | 38.7% | 60% | 80% | 80%+ |
| PM10 Detection | ❌ | ✅ | ✅ | ✅ |

### API Performance

| Metric | Current | Target |
|--------|---------|--------|
| Health Endpoint | ✅ 100% | ✅ 100% |
| Wards Endpoint | ✅ 100% | ✅ 100% |
| Forecast Endpoint | ❌ 0% | ✅ 100% |
| Navigation Endpoint | ❌ 0% | ✅ 100% |
| GEE Endpoint | ⚠️ 50% | ✅ 100% |

---

## 🎯 Daily Checklist Template

### Daily Standup Questions
1. What did I complete yesterday?
2. What will I work on today?
3. Any blockers?

### Daily Tasks
- [ ] Check model training progress
- [ ] Review validation metrics
- [ ] Update progress in tracking doc
- [ ] Commit code changes
- [ ] Update documentation

---

## 🚨 Risk Management

### Potential Risks

1. **Data Quality Issues**
   - **Risk:** Historical data has too many missing values
   - **Mitigation:** Use multiple data sources, implement robust imputation
   - **Contingency:** Use synthetic data augmentation

2. **Model Training Time**
   - **Risk:** Training takes longer than expected
   - **Mitigation:** Use GPU, optimize batch size
   - **Contingency:** Reduce model complexity

3. **API Integration Failures**
   - **Risk:** WAQI/OpenAQ APIs are down
   - **Mitigation:** Implement caching, fallback mechanisms
   - **Contingency:** Use cached data, show warnings

4. **Deployment Issues**
   - **Risk:** New model breaks production
   - **Mitigation:** Thorough testing, gradual rollout
   - **Contingency:** Quick rollback plan

---

## 📝 Deliverables Checklist

### Week 1 Deliverables
- [ ] Security audit complete
- [ ] All secrets rotated
- [ ] Training data collected (10,000+ records)
- [ ] Data preprocessing complete

### Week 2 Deliverables
- [ ] Feature engineering complete
- [ ] Model trained and saved
- [ ] API endpoints fixed
- [ ] Validation metrics documented

### Week 3 Deliverables
- [ ] Model evaluation report
- [ ] New model integrated
- [ ] Validation tests passing
- [ ] Accuracy > 80%

### Week 4 Deliverables
- [ ] Confidence intervals implemented
- [ ] Multi-source integration complete
- [ ] Dwarka validation successful
- [ ] Production deployment complete
- [ ] Documentation updated

---

## 💻 Commands Quick Reference

### Data Collection
```bash
cd backend/scripts
python collect_training_data.py
python download_openaq_data.py
python collect_dwarka_data.py
```

### Data Preprocessing
```bash
python preprocess_training_data.py
python create_features.py
```

### Model Training
```bash
python train_improved_model.py
```

### Model Evaluation
```bash
python evaluate_model.py
```

### Testing
```bash
cd backend
python test_aqi_validation.py
python test_end_to_end.py
```

### Deployment
```bash
# Copy new model files
cp scripts/improved_model_best.pt app/services/
cp scripts/improved_scaler.pkl app/services/

# Restart backend
# (depends on your deployment method)
```

---

## 📞 Team Contacts

### Roles & Responsibilities

**Project Manager:**
- Track progress
- Remove blockers
- Stakeholder communication

**Data Engineer:**
- Data collection
- Data preprocessing
- Data quality

**Data Scientist:**
- Feature engineering
- Model training
- Model evaluation

**ML Engineer:**
- Model optimization
- Model integration
- Performance tuning

**Backend Developer:**
- API fixes
- Model deployment
- Integration testing

**DevOps:**
- Security hardening
- Infrastructure
- Deployment

---

## 📈 Progress Tracking

### Week 1 Progress: ___% Complete
- Security: ☐ Not Started | ☐ In Progress | ☐ Complete
- Data Collection: ☐ Not Started | ☐ In Progress | ☐ Complete
- Preprocessing: ☐ Not Started | ☐ In Progress | ☐ Complete

### Week 2 Progress: ___% Complete
- Feature Engineering: ☐ Not Started | ☐ In Progress | ☐ Complete
- Model Training: ☐ Not Started | ☐ In Progress | ☐ Complete
- API Fixes: ☐ Not Started | ☐ In Progress | ☐ Complete

### Week 3 Progress: ___% Complete
- Model Evaluation: ☐ Not Started | ☐ In Progress | ☐ Complete
- Integration: ☐ Not Started | ☐ In Progress | ☐ Complete
- Testing: ☐ Not Started | ☐ In Progress | ☐ Complete

### Week 4 Progress: ___% Complete
- Confidence Intervals: ☐ Not Started | ☐ In Progress | ☐ Complete
- Multi-Source: ☐ Not Started | ☐ In Progress | ☐ Complete
- Deployment: ☐ Not Started | ☐ In Progress | ☐ Complete

---

## ✅ Final Checklist

Before marking project complete:

- [ ] All accuracy targets met
- [ ] All API endpoints working
- [ ] Security audit passed
- [ ] Documentation updated
- [ ] Tests passing
- [ ] Production deployment successful
- [ ] Monitoring in place
- [ ] Team trained on new features

---

**Status:** Ready to begin  
**Next Action:** Start Week 1, Day 1 - Security Hardening  
**Review Date:** End of each week
