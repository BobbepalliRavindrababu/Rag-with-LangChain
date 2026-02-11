"""
Test Suite for RAG System Components
"""
import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from document_processor import DocumentProcessor
from chunker import TextChunker
from vector_store import VectorStore
from retriever import Retriever
from answer_generator import AnswerGenerator


class TestDocumentProcessor(unittest.TestCase):
    """Test document processing functionality"""
    
    def setUp(self):
        self.processor = DocumentProcessor()
        # Create a test file
        self.test_file = "test_doc.txt"
        with open(self.test_file, 'w') as f:
            f.write("This is a test document for RAG system.")
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_load_txt_document(self):
        """Test loading TXT files"""
        content = self.processor.load_document(self.test_file)
        self.assertIsNotNone(content)
        self.assertIn("test document", content)
    
    def test_unsupported_format(self):
        """Test handling of unsupported file formats"""
        with self.assertRaises(ValueError):
            self.processor.load_document("test.xyz")


class TestChunker(unittest.TestCase):
    """Test text chunking functionality"""
    
    def setUp(self):
        self.chunker = TextChunker(chunk_size=100, overlap=20)
    
    def test_basic_chunking(self):
        """Test basic text chunking"""
        text = "This is a test. " * 20
        chunks = self.chunker.chunk_text(text, "test")
        
        self.assertGreater(len(chunks), 0)
        self.assertTrue(all('text' in c for c in chunks))
        self.assertTrue(all('source' in c for c in chunks))
    
    def test_chunk_overlap(self):
        """Test that chunks have overlap"""
        text = "Sentence one. Sentence two. Sentence three. " * 10
        chunks = self.chunker.chunk_text(text, "test")
        
        if len(chunks) > 1:
            # Check that some content appears in multiple chunks
            first_end = chunks[0]['text'][-50:]
            second_start = chunks[1]['text'][:100]
            # There should be some overlap
            self.assertTrue(len(chunks) >= 2)


class TestVectorStore(unittest.TestCase):
    """Test vector store functionality"""
    
    def setUp(self):
        self.store = VectorStore()
        self.test_chunks = [
            {'id': 0, 'text': 'Python is a programming language.', 'source': 'test.txt'},
            {'id': 1, 'text': 'Machine learning uses algorithms.', 'source': 'test.txt'},
        ]
    
    def test_add_chunks(self):
        """Test adding chunks to vector store"""
        self.store.add_chunks(self.test_chunks)
        stats = self.store.get_stats()
        
        self.assertEqual(stats['total_chunks'], 2)
        self.assertIsNotNone(self.store.index)
    
    def test_search(self):
        """Test vector similarity search"""
        self.store.add_chunks(self.test_chunks)
        results = self.store.search("What is Python?", top_k=1)
        
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0][1], float)  # similarity score


class TestAnswerGenerator(unittest.TestCase):
    """Test answer generation functionality"""
    
    def setUp(self):
        self.generator = AnswerGenerator()
        self.test_chunks = [
            {
                'text': 'Python is a high-level programming language.',
                'score': 0.9,
                'source': 'test.txt',
                'chunk_id': 0
            }
        ]
    
    def test_generate_answer(self):
        """Test answer generation"""
        answer = self.generator.generate_answer(
            "What is Python?",
            self.test_chunks
        )
        
        self.assertIn('answer', answer)
        self.assertIn('confidence', answer)
        self.assertIn('sources', answer)
        self.assertIsInstance(answer['confidence'], float)
    
    def test_definition_query_detection(self):
        """Test detection of definition queries"""
        self.assertTrue(self.generator._is_definition_query("what is machine learning"))
        self.assertTrue(self.generator._is_definition_query("define neural network"))
        self.assertFalse(self.generator._is_definition_query("how to train a model"))
    
    def test_empty_chunks(self):
        """Test handling of empty chunks"""
        answer = self.generator.generate_answer("Test question", [])
        self.assertEqual(answer['confidence'], 0.0)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running RAG System Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestChunker))
    suite.addTests(loader.loadTestsFromTestCase(TestVectorStore))
    suite.addTests(loader.loadTestsFromTestCase(TestAnswerGenerator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
