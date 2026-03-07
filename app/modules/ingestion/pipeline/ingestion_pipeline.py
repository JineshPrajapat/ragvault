from app.modules.ingestion.loaders.pdf_loader import PDFLoader
from app.modules.ingestion.extractors.docling_extractor import DoclingExtractor
from app.modules.ingestion.processors.density_analyzer import DensityAnalyzer
from app.modules.ingestion.processors.markdown_builder import MarkdownBuilder
from app.modules.ingestion.processors.structure_analyzer import StructureAnalyzer
from app.modules.ingestion.processors.section_builder import SectionBuilder
from app.modules.ingestion.processors.metadata_builder import MetadataBuilder
from app.modules.ingestion.processors.keyword_extractor import KeywordExtractor
from app.modules.ingestion.chunking.semantic_chunker import SemanticChunker
from app.modules.ingestion.processors.content_cleaner import ContentCleaner

class IngestionPipeline:

    def __init__(self):

        self.loader = PDFLoader()
        self.density   = DensityAnalyzer()
        self.extractor = DoclingExtractor()
        self.structure = StructureAnalyzer()
        self.section_builder = SectionBuilder()
        self.markdown_builder = MarkdownBuilder()
        self.cleaner = ContentCleaner()
        self.metadata_builder = MetadataBuilder()
        self.keyword_extractor = KeywordExtractor()
        self.chunker = SemanticChunker()

    def run(self, file_path: str):

        # Load document
        document = self.loader.load(file_path)

        profile = self.density.analyze(document)
        print("profile", profile)

        # Extract layout elements
        layout = self.extractor.extract(document)
        if not layout:
            print("No elements extracted from document")
            return []
        
        print("layout length", len(layout))

        # Analyze structure
        structure = self.structure.analyze(document, layout)
        print("structure")
        sections = self.section_builder.build(layout, structure)
        sections = self.markdown_builder.build(sections)

        # Clean content
        sections = self.cleaner.clean(sections)
        print("cleaned sections.......", len(sections))

        # Add metadata and keywords
        enriched_sections = self.metadata_builder.build(sections)
        print("metadata, ", len(enriched_sections))
        enriched_sections = self.keyword_extractor.extract(enriched_sections)
        print("enriched_sections, ", enriched_sections[2])

        # Chunk sections
        print("chunking sections.......")
        
        chunks = self.chunker.chunk(enriched_sections)

        print("chunks length", len(chunks))

        return chunks