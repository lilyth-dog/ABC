import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import CultureSelector, { CULTURAL_CONTEXTS } from '../components/CultureSelector'

describe('CultureSelector Component', () => {
    const mockOnCultureChange = vi.fn()

    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders trigger button', () => {
        render(
            <CultureSelector
                selectedCulture="default"
                onCultureChange={mockOnCultureChange}
            />
        )

        const trigger = document.querySelector('.culture-trigger')
        expect(trigger).toBeInTheDocument()
    })

    it('shows current culture flag', () => {
        render(
            <CultureSelector
                selectedCulture="east_asian"
                onCultureChange={mockOnCultureChange}
            />
        )

        expect(screen.getByText('🇰🇷')).toBeInTheDocument()
    })

    it('opens dropdown when clicked', () => {
        render(
            <CultureSelector
                selectedCulture="default"
                onCultureChange={mockOnCultureChange}
            />
        )

        const trigger = document.querySelector('.culture-trigger')!
        fireEvent.click(trigger)

        const dropdown = document.querySelector('.culture-dropdown')
        expect(dropdown).toBeInTheDocument()
    })

    it('displays all available cultures in dropdown', () => {
        render(
            <CultureSelector
                selectedCulture="default"
                onCultureChange={mockOnCultureChange}
            />
        )

        const trigger = document.querySelector('.culture-trigger')!
        fireEvent.click(trigger)

        CULTURAL_CONTEXTS.forEach(culture => {
            const elements = screen.getAllByText(culture.name)
            expect(elements.length).toBeGreaterThan(0)
        })
    })

    it('calls onCultureChange when option is selected', () => {
        render(
            <CultureSelector
                selectedCulture="default"
                onCultureChange={mockOnCultureChange}
            />
        )

        const trigger = document.querySelector('.culture-trigger')!
        fireEvent.click(trigger)

        const eastAsianOption = screen.getByText('동아시아')
        fireEvent.click(eastAsianOption)

        expect(mockOnCultureChange).toHaveBeenCalledWith('east_asian')
    })

    it('shows check mark for selected culture', () => {
        render(
            <CultureSelector
                selectedCulture="western"
                onCultureChange={mockOnCultureChange}
            />
        )

        const trigger = document.querySelector('.culture-trigger')!
        fireEvent.click(trigger)

        const selectedOption = document.querySelector('.culture-option.selected')
        expect(selectedOption).toBeInTheDocument()
    })

    it('renders in compact mode when specified', () => {
        render(
            <CultureSelector
                selectedCulture="default"
                onCultureChange={mockOnCultureChange}
                compact={true}
            />
        )

        const trigger = document.querySelector('.culture-trigger.compact')
        expect(trigger).toBeInTheDocument()
    })
})
