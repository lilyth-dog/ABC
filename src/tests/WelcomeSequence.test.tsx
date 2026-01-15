import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import WelcomeSequence from '../components/WelcomeSequence'

// Mock AudioManager context
vi.mock('../components/AudioManager', () => ({
    useAudio: () => ({
        playChime: vi.fn(),
    }),
}))

describe('WelcomeSequence Component', () => {
    const mockOnComplete = vi.fn()

    beforeEach(() => {
        vi.clearAllMocks()
        vi.useFakeTimers()
    })

    afterEach(() => {
        vi.useRealTimers()
    })

    it('renders welcome overlay', () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        const overlay = document.querySelector('.welcome-overlay')
        expect(overlay).toBeInTheDocument()
    })

    it('shows soul orb visual element', () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        const soulOrb = document.querySelector('.soul-orb')
        expect(soulOrb).toBeInTheDocument()
    })

    it('displays typing animation', async () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        // Fast-forward timers to see typing progress
        await act(async () => {
            vi.advanceTimersByTime(500)
        })

        const messageElement = document.querySelector('.message')
        expect(messageElement).toBeInTheDocument()
    })

    it('has particle field for visual effect', () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        const particleField = document.querySelector('.particle-field')
        expect(particleField).toBeInTheDocument()
    })

    it('shows progress dots', () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        const progressDots = document.querySelectorAll('.progress-dot')
        expect(progressDots.length).toBeGreaterThan(0)
    })

    it('calls onComplete after animation finishes', async () => {
        render(<WelcomeSequence onComplete={mockOnComplete} />)

        // Advance in increments to satisfy multiple nested setTimeouts/intervals
        await act(async () => {
            for (let i = 0; i < 100; i++) {
                vi.advanceTimersByTime(1000)
            }
        })

        await waitFor(() => {
            expect(mockOnComplete).toHaveBeenCalled()
        }, { timeout: 10000 })
    })
})
