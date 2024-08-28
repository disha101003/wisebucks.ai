import React, { useState } from 'react';

const FormStepper = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});

  const steps = [
    <div key="step1" className={currentStep === 0 ? 'step active' : 'step'}>Step 1 Content</div>,
    <div key="step2" className={currentStep === 1 ? 'step active' : 'step'}>Step 2 Content</div>,
    <div key="step3" className={currentStep === 2 ? 'step active' : 'step'}>Step 3 Content</div>,
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    setFormData({});
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {steps}
      <div>
        <button type="button" onClick={handlePrev} disabled={currentStep === 0}>Previous</button>
        <button type="button" onClick={handleNext} disabled={currentStep === steps.length - 1}>Next</button>
      </div>
      <div>
        <button type="submit">Submit</button>
      </div>
      <input type="text" name="exampleField" onChange={handleInputChange} />
    </form>
  );
};

export default FormStepper;
