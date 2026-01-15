import '@testing-library/jest-dom'

// Mock AudioContext for tests
class MockAudioContext {
    createOscillator() {
        return {
            type: 'sine',
            frequency: { setValueAtTime: () => { } },
            connect: () => { },
            start: () => { },
            stop: () => { },
        }
    }
    createGain() {
        return {
            gain: { setValueAtTime: () => { }, linearRampToValueAtTime: () => { } },
            connect: () => { },
        }
    }
    get destination() {
        return {}
    }
    get currentTime() {
        return 0
    }
}

// @ts-ignore
global.AudioContext = MockAudioContext
// @ts-ignore  
global.webkitAudioContext = MockAudioContext

// Mock localStorage
const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
}
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

// Mock fetch
global.fetch = vi.fn()
