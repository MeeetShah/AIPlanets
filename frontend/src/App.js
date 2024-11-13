
import './App.css';

import PdfUpload from "./components/PdfUpload";
import PdfList from "./components/PdfList";
import QuestionForm from './components/QuestionForm';

function App() {
  return (
    <div>
      
      <PdfUpload />
      <PdfList />
      <QuestionForm/>
    </div>
    
  );
}

export default App;
