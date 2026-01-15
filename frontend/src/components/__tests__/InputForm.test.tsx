import { render, screen, fireEvent } from '@testing-library/react';
import { InputForm } from '../InputForm';
import { vi } from 'vitest';

describe('InputForm Component', () => {
    it('renders correctly', () => {
        render(<InputForm onGenerate={() => { }} isLoading={false} />);
        expect(screen.getByPlaceholderText(/Paste raw spec here/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Generate Test Steps/i })).toBeInTheDocument();
    });

    it('calls onGenerate when submitted with text', () => {
        const mockHandler = vi.fn();
        render(<InputForm onGenerate={mockHandler} isLoading={false} />);

        const textarea = screen.getByPlaceholderText(/Paste raw spec here/i);
        const button = screen.getByRole('button');

        // Simulate typing
        fireEvent.change(textarea, { target: { value: 'Test Spec' } });
        // Simulate click
        fireEvent.click(button);

        expect(mockHandler).toHaveBeenCalledTimes(1);
        expect(mockHandler).toHaveBeenCalledWith('Test Spec');
    });

    it('disables button when loading', () => {
        render(<InputForm onGenerate={() => { }} isLoading={true} />);
        const button = screen.getByRole('button');
        expect(button).toBeDisabled();
        expect(button).toHaveTextContent('Generating Procedure...');
    });
});