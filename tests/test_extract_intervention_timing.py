import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from extract_intervention_timing import find_timing_sentences  # noqa: E402

XML = b"""<?xml version="1.0"?>
<article><front><article-meta><title-group><article-title>T</article-title></title-group></article-meta></front>
<body>
 <sec><title>Methods</title>
  <sec><title>ASO treatment</title>
   <p>Neurons were treated with ASO on day 3. Cells were imaged with a confocal microscope.</p>
   <p>Doxycycline was added at DIV 10; recordings followed.</p>
  </sec>
 </sec>
 <sec><title>Results</title>
  <p>TDP-43 was reduced. No timing here for the intervention.</p>
  <fig><label>Figure 1</label><caption><p>Mice were injected with AAV at P1 and tested at 6 months.</p></caption></fig>
 </sec>
</body></article>"""


class TimingExtractionTest(unittest.TestCase):
    def setUp(self):
        self.hits = find_timing_sentences(XML)
        self.sentences = [h["sentence"] for h in self.hits]

    def test_finds_intervention_with_time(self):
        self.assertIn("Neurons were treated with ASO on day 3.", self.sentences)
        self.assertTrue(any("Doxycycline was added at DIV 10" in s for s in self.sentences))

    def test_keeps_section_path_and_figure_caption(self):
        sections = {h["section"] for h in self.hits}
        self.assertIn("Methods > ASO treatment", sections)
        self.assertTrue(any("Figure 1" in s for s in sections))

    def test_ignores_sentences_without_intervention_or_time(self):
        self.assertNotIn("Cells were imaged with a confocal microscope.", self.sentences)
        self.assertFalse(any(s.startswith("TDP-43 was reduced") for s in self.sentences))


if __name__ == "__main__":
    unittest.main()
