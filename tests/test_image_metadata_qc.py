import struct,unittest
from scripts.image_metadata_qc import parse_tiff,validate_range
class ImageMetadataTests(unittest.TestCase):
 def fixture(self,endian):
  magic=b'MM' if endian=='>' else b'II'
  entries=[struct.pack(endian+'HHII',256,4,1,100),struct.pack(endian+'HHII',257,4,1,200),
           struct.pack(endian+'HHI',258,3,1)+struct.pack(endian+'H',16)+b'\0\0']
  return magic+struct.pack(endian+'HI',42,8)+struct.pack(endian+'H',3)+b''.join(entries)+struct.pack(endian+'I',0)
 def test_big_and_little_endian_inline_short(self):
  for e in ['>','<']:
   r=parse_tiff(self.fixture(e));self.assertEqual((r['width'],r['height'],r['bits']),(100,200,16))
 def test_no_resolution_is_not_pixel_scale_one(self):
  r=parse_tiff(self.fixture('>'));self.assertIsNone(r['x_resolution']);self.assertIsNone(r['resolution_unit'])
 def test_truncated_ifd_rejected(self):
  with self.assertRaises(ValueError):parse_tiff(self.fixture('>')[:20])
 def test_bigtiff_not_silently_read_as_classic(self):
  with self.assertRaises(ValueError):parse_tiff(b'II'+struct.pack('<HI',43,8))
 def test_range_ignored_rejected(self):
  with self.assertRaises(ValueError):validate_range(200,'bytes 0-3/20',0,3,20,b'1234')
 def test_wrong_object_size_rejected(self):
  with self.assertRaises(ValueError):validate_range(206,'bytes 0-3/19',0,3,20,b'1234')
 def test_truncated_response_rejected(self):
  with self.assertRaises(ValueError):validate_range(206,'bytes 0-3/20',0,3,20,b'12')
 def test_valid_range(self):validate_range(206,'bytes 0-3/20',0,3,20,b'1234')

class PhysicalScaleTests(unittest.TestCase):
 def test_imagej_micron_rational(self):
  from scripts.image_metadata_qc import micron_scale
  d=micron_scale({'description':'unit=micron\n','x_resolution':[3076923,1000000],'y_resolution':[3076923,1000000]})
  self.assertAlmostEqual(d['x_um_per_pixel'],.325,places=6)
 def test_no_unit_no_physical_scale(self):
  from scripts.image_metadata_qc import micron_scale
  self.assertIsNone(micron_scale({'description':'ImageJ=1.54f','x_resolution':[1,1],'y_resolution':[1,1]}))
 def test_zero_rational_rejected(self):
  from scripts.image_metadata_qc import micron_scale
  self.assertIsNone(micron_scale({'description':'unit=micron','x_resolution':[0,1],'y_resolution':[1,1]}))
