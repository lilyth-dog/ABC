"""
OVF (OOMMF Vector Field) 파일 파서
MuMax3 시뮬레이션 결과 파일을 읽기 위한 파서

OVF 파일 형식:
- 텍스트 헤더 (메타데이터)
- 바이너리 데이터 (벡터 필드)
"""
import struct
import numpy as np
from typing import Dict, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class OVFParser:
    """
    OVF 파일 파서 클래스
    MuMax3 출력 파일을 읽어서 numpy 배열로 변환
    """
    
    def __init__(self):
        self.supported_versions = ["OOMMF: rectangular mesh v1.0"]
    
    def parse_ovf(self, file_path: str) -> Optional[np.ndarray]:
        """
        OVF 파일 파싱
        
        Args:
            file_path: OVF 파일 경로
        
        Returns:
            3D numpy 배열 (nx, ny, nz, 3) - 자기화 벡터 필드
            또는 None (파싱 실패 시)
        """
        try:
            with open(file_path, 'rb') as f:
                # 헤더 읽기
                header = self._read_header(f)
                if not header:
                    return None
                
                # 데이터 읽기
                data = self._read_data(f, header)
                return data
                
        except FileNotFoundError:
            logger.error(f"OVF file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Failed to parse OVF file: {e}")
            return None
    
    def _read_header(self, file_handle) -> Optional[Dict]:
        """OVF 파일 헤더 읽기"""
        header = {}
        header_end = False
        
        while not header_end:
            line = file_handle.readline()
            if not line:
                return None
            
            # 텍스트 모드로 디코딩
            try:
                line_str = line.decode('utf-8', errors='ignore').strip()
            except:
                line_str = line.decode('latin-1', errors='ignore').strip()
            
            # 헤더 종료 확인
            if line_str.startswith('# Begin: Data'):
                header_end = True
                break
            
            # 주석 제거
            if line_str.startswith('#'):
                line_str = line_str[1:].strip()
            
            # 키-값 쌍 파싱
            if ':' in line_str:
                key, value = line_str.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 주요 필드 파싱
                if key == 'Segment count':
                    header['segment_count'] = int(value)
                elif key == 'Begin: Segment':
                    header['segment_start'] = True
                elif key == 'Title':
                    header['title'] = value
                elif key == 'meshtype':
                    header['meshtype'] = value
                elif key == 'xmin' or key == 'ymin' or key == 'zmin':
                    header[key] = float(value)
                elif key == 'xmax' or key == 'ymax' or key == 'zmax':
                    header[key] = float(value)
                elif key == 'xbase' or key == 'ybase' or key == 'zbase':
                    header[key] = float(value)
                elif key == 'xnodes' or key == 'ynodes' or key == 'znodes':
                    header[key] = int(value)
                elif key == 'xstepsize' or key == 'ystepsize' or key == 'zstepsize':
                    header[key] = float(value)
                elif key == 'valuedim':
                    header['valuedim'] = int(value)
                elif key == 'valuelabels':
                    header['valuelabels'] = value.split()
                elif key == 'valueunits':
                    header['valueunits'] = value.split()
                elif key == 'Datacount':
                    header['datacount'] = int(value)
        
        # 기본값 설정
        if 'xnodes' not in header:
            header['xnodes'] = 128  # 기본값
        if 'ynodes' not in header:
            header['ynodes'] = 128
        if 'znodes' not in header:
            header['znodes'] = 1
        if 'valuedim' not in header:
            header['valuedim'] = 3  # 벡터 필드
        
        return header
    
    def _read_data(self, file_handle, header: Dict) -> Optional[np.ndarray]:
        """OVF 파일 데이터 읽기"""
        try:
            nx = header.get('xnodes', 128)
            ny = header.get('ynodes', 128)
            nz = header.get('znodes', 1)
            valuedim = header.get('valuedim', 3)
            datacount = header.get('datacount', nx * ny * nz)
            
            # 바이너리 데이터 읽기
            # OVF는 보통 텍스트 형식이지만, 바이너리도 지원
            # 여기서는 텍스트 형식 가정
            
            data_list = []
            line_count = 0
            
            while line_count < datacount:
                line = file_handle.readline()
                if not line:
                    break
                
                # 텍스트 디코딩
                try:
                    line_str = line.decode('utf-8', errors='ignore').strip()
                except:
                    line_str = line.decode('latin-1', errors='ignore').strip()
                
                # 주석이나 빈 줄 건너뛰기
                if not line_str or line_str.startswith('#'):
                    continue
                
                # 데이터 파싱
                try:
                    values = [float(x) for x in line_str.split()]
                    if len(values) >= valuedim:
                        data_list.append(values[:valuedim])
                        line_count += 1
                except ValueError:
                    continue
            
            if not data_list:
                logger.warning("No data found in OVF file")
                return None
            
            # numpy 배열로 변환
            data_array = np.array(data_list)
            
            # 형태 재구성 (nx, ny, nz, valuedim)
            if len(data_array) == nx * ny * nz:
                data_array = data_array.reshape((nx, ny, nz, valuedim))
            else:
                # 데이터가 부족하면 패딩 또는 리샘플링
                logger.warning(f"Data count mismatch: expected {nx*ny*nz}, got {len(data_array)}")
                # 간단한 리샘플링
                if len(data_array) > 0:
                    # 2D로 변환 (z=1인 경우)
                    if nz == 1:
                        target_size = nx * ny
                        if len(data_array) < target_size:
                            # 패딩
                            padding = np.zeros((target_size - len(data_array), valuedim))
                            data_array = np.vstack([data_array, padding])
                        elif len(data_array) > target_size:
                            # 다운샘플링
                            indices = np.linspace(0, len(data_array)-1, target_size, dtype=int)
                            data_array = data_array[indices]
                        
                        data_array = data_array[:target_size].reshape((nx, ny, valuedim))
                    else:
                        data_array = data_array.reshape((nx, ny, nz, valuedim))
            
            return data_array
            
        except Exception as e:
            logger.error(f"Failed to read OVF data: {e}")
            return None
    
    def extract_magnetization_magnitude(self, ovf_data: np.ndarray) -> np.ndarray:
        """
        자기화 벡터 필드에서 크기 추출
        
        Args:
            ovf_data: (nx, ny, nz, 3) 형태의 벡터 필드
        
        Returns:
            (nx, ny, nz) 형태의 스칼라 필드
        """
        if ovf_data is None or len(ovf_data.shape) != 4:
            return None
        
        # 벡터 크기 계산
        magnitude = np.linalg.norm(ovf_data, axis=-1)
        return magnitude
    
    def extract_z_component(self, ovf_data: np.ndarray) -> np.ndarray:
        """
        z-성분만 추출 (2D 시각화용)
        
        Args:
            ovf_data: (nx, ny, nz, 3) 형태의 벡터 필드
        
        Returns:
            (nx, ny) 형태의 스칼라 필드
        """
        if ovf_data is None:
            return None
        
        if len(ovf_data.shape) == 4:
            # z=0 슬라이스, z-성분
            if ovf_data.shape[2] > 0:
                return ovf_data[:, :, 0, 2]
            else:
                return ovf_data[:, :, 0, 2]
        elif len(ovf_data.shape) == 3:
            # 이미 2D인 경우
            return ovf_data[:, :, 2] if ovf_data.shape[2] >= 3 else ovf_data[:, :, 0]
        
        return None


# 전역 인스턴스
_ovf_parser: Optional[OVFParser] = None


def get_ovf_parser() -> OVFParser:
    """OVF 파서 인스턴스 가져오기"""
    global _ovf_parser
    if _ovf_parser is None:
        _ovf_parser = OVFParser()
    return _ovf_parser


if __name__ == "__main__":
    # 테스트
    parser = get_ovf_parser()
    print("OVF Parser initialized")
    print(f"Supported versions: {parser.supported_versions}")
