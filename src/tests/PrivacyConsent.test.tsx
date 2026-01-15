import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import PrivacyConsent from '../components/PrivacyConsent'

// Mock AudioManager context
vi.mock('../components/AudioManager', () => ({
    useAudio: () => ({
        playChime: vi.fn(),
        playSuccess: vi.fn(),
    }),
}))

describe('PrivacyConsent Component', () => {
    const mockUserId = 'test-user-123'
    const mockOnConsent = vi.fn()
    const mockOnClose = vi.fn()

    beforeEach(() => {
        vi.clearAllMocks()
        // @ts-ignore
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'saved', consent_id: 1 }),
            })
        )
    })

    it('renders privacy consent title', () => {
        render(
            <PrivacyConsent
                userId={mockUserId}
                onConsent={mockOnConsent}
                onClose={mockOnClose}
            />
        )

        expect(screen.getByText(/개인정보 보호 및 동의/i)).toBeInTheDocument()
    })

    it('shows required consent toggles', () => {
        render(
            <PrivacyConsent
                userId={mockUserId}
                onConsent={mockOnConsent}
                onClose={mockOnClose}
            />
        )

        expect(screen.getByText(/행동 데이터 수집/i)).toBeInTheDocument()
        expect(screen.getByText(/프로필 저장/i)).toBeInTheDocument()
        expect(screen.getByText(/지속적 학습/i)).toBeInTheDocument()
    })

    it('calls onClose when decline button is clicked', () => {
        render(
            <PrivacyConsent
                userId={mockUserId}
                onConsent={mockOnConsent}
                onClose={mockOnClose}
            />
        )

        const declineButton = screen.getByText(/거부/i)
        fireEvent.click(declineButton)

        expect(mockOnClose).toHaveBeenCalledTimes(1)
    })

    it('submits consent when agree button is clicked', async () => {
        render(
            <PrivacyConsent
                userId={mockUserId}
                onConsent={mockOnConsent}
                onClose={mockOnClose}
            />
        )

        const agreeButton = screen.getByText(/동의하고 시작하기/i)
        fireEvent.click(agreeButton)

        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/user/'),
                expect.objectContaining({
                    method: 'POST',
                })
            )
        })

        await waitFor(() => {
            expect(mockOnConsent).toHaveBeenCalledWith(true)
        })
    })

    it('displays GDPR information', () => {
        render(
            <PrivacyConsent
                userId={mockUserId}
                onConsent={mockOnConsent}
                onClose={mockOnClose}
            />
        )

        expect(screen.getByText(/동의를 철회/i)).toBeInTheDocument()
    })
})
