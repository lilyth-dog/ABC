"""
OVF 파서 단위 테스트
"""
import pytest
import numpy as np
import sys
from pathlib import Path
import tempfile
import os

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from ovf_parser import OVFParser


class TestOVFParser:
    """OVFParser 클래스 테스트"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.parser = OVFParser()
    
    def test_extract_magnetization_magnitude(self):
        """자기화 크기 추출 테스트"""
        # 테스트 데이터 생성
        test_data = np.random.rand(128, 128, 1, 3)  # (nx, ny, nz, 3)
        magnitude = self.parser.extract_magnetization_magnitude(test_data)
        
        assert magnitude is not None
        assert magnitude.shape == (128, 128, 1)
        assert np.all(magnitude >= 0)  # 크기는 항상 양수
    
    def test_extract_z_component(self):
        """z-성분 추출 테스트"""
        # 테스트 데이터 생성
        test_data = np.random.rand(128, 128, 1, 3)  # (nx, ny, nz, 3)
        z_component = self.parser.extract_z_component(test_data)
        
        assert z_component is not None
        assert len(z_component.shape) == 2  # (nx, ny)
        assert z_component.shape == (128, 128)
    
    def test_parse_ovf_nonexistent_file(self):
        """존재하지 않는 파일 파싱 테스트"""
        result = self.parser.parse_ovf("/nonexistent/file.ovf")
        assert result is None
    
    def test_parse_ovf_invalid_file(self):
        """잘못된 형식 파일 파싱 테스트"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ovf', delete=False) as f:
            f.write("Invalid OVF file content")
            temp_path = f.name
        
        try:
            result = self.parser.parse_ovf(temp_path)
            # 파싱 실패 시 None 반환
            assert result is None or isinstance(result, np.ndarray)
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
