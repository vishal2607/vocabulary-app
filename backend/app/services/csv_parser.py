"""CSV Parser service for parsing vocabulary CSV files."""
import csv
import io
from typing import List, Optional, Tuple
from dataclasses import dataclass
import chardet
import pandas as pd


@dataclass
class ParseResult:
    """Result of CSV parsing operation.
    
    Attributes:
        entries: List of parsed vocabulary entry dictionaries
        errors: List of error messages encountered during parsing
        warnings: List of warning messages
        total_rows: Total number of rows in the CSV (excluding header)
        successful_rows: Number of rows successfully parsed
    """
    entries: List[dict]
    errors: List[str]
    warnings: List[str]
    total_rows: int
    successful_rows: int


class CSVParseError(Exception):
    """Exception raised when CSV parsing fails."""
    pass


class CSVParser:
    """Service for parsing CSV files containing vocabulary data.
    
    Supports:
    - Multiple encodings (UTF-8, UTF-16, ASCII)
    - Multiple delimiters (comma, semicolon, tab)
    - Header detection and column mapping
    - Robust error handling for malformed data
    """
    
    # Expected column names (case-insensitive)
    EXPECTED_COLUMNS = ['word', 'meaning', 'synonym', 'pronunciation', 'example']
    REQUIRED_COLUMNS = ['word', 'meaning']
    
    # Supported delimiters
    DELIMITERS = [',', ';', '\t']
    
    # Supported encodings
    ENCODINGS = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'ascii', 'latin-1']
    
    def detect_encoding(self, file_content: bytes) -> str:
        """Detect the encoding of a file from its byte content.
        
        Uses chardet library to detect encoding with fallback to UTF-8.
        Supports UTF-8, UTF-16 (with BOM variants), ASCII, and Latin-1.
        
        Args:
            file_content: Raw bytes of the file
            
        Returns:
            str: Detected encoding name (e.g., 'utf-8', 'utf-16')
            
        Raises:
            CSVParseError: If encoding cannot be detected
        """
        if not file_content:
            raise CSVParseError("File is empty")
        
        # Try to detect encoding using chardet
        detection = chardet.detect(file_content)
        detected_encoding = detection.get('encoding')
        confidence = detection.get('confidence', 0)
        
        if detected_encoding and confidence > 0.7:
            # Normalize encoding name
            detected_encoding = detected_encoding.lower()
            
            # Map common encoding variations
            if detected_encoding in ['utf-8', 'utf8']:
                return 'utf-8'
            elif detected_encoding in ['utf-16', 'utf16', 'utf-16-le', 'utf-16-be']:
                return detected_encoding
            elif detected_encoding in ['ascii', 'us-ascii']:
                return 'ascii'
            elif detected_encoding in ['iso-8859-1', 'latin-1', 'latin1']:
                return 'latin-1'
        
        # Try to decode with common encodings
        for encoding in self.ENCODINGS:
            try:
                file_content.decode(encoding)
                return encoding
            except (UnicodeDecodeError, LookupError):
                continue
        
        # Default to UTF-8 if nothing else works
        return 'utf-8'
    
    def detect_delimiter(self, sample: str) -> str:
        """Detect the delimiter used in a CSV file from a sample.
        
        Analyzes the first few lines to determine if comma, semicolon,
        or tab is used as the delimiter.
        
        Args:
            sample: Sample text from the CSV file (first few lines)
            
        Returns:
            str: Detected delimiter character (',', ';', or '\\t')
            
        Raises:
            CSVParseError: If delimiter cannot be detected
        """
        if not sample:
            raise CSVParseError("Cannot detect delimiter from empty sample")
        
        # Use csv.Sniffer to detect delimiter
        try:
            sniffer = csv.Sniffer()
            # Get first few lines for analysis
            lines = sample.split('\n')[:5]
            sample_text = '\n'.join(lines)
            
            if sample_text.strip():
                dialect = sniffer.sniff(sample_text, delimiters=',;\t')
                return dialect.delimiter
        except csv.Error:
            pass
        
        # Fallback: count occurrences of each delimiter
        delimiter_counts = {}
        lines = sample.split('\n')[:5]
        
        for delimiter in self.DELIMITERS:
            # Count delimiter occurrences in each line
            counts = [line.count(delimiter) for line in lines if line.strip()]
            if counts:
                # Check if delimiter appears consistently
                avg_count = sum(counts) / len(counts)
                consistency = all(abs(c - avg_count) <= 1 for c in counts)
                if consistency and avg_count > 0:
                    delimiter_counts[delimiter] = avg_count
        
        if delimiter_counts:
            # Return delimiter with highest consistent count
            return max(delimiter_counts, key=delimiter_counts.get)
        
        # Default to comma
        return ','
    
    def _detect_header(self, lines: List[str], delimiter: str) -> bool:
        """Detect if the first line is a header row.
        
        Args:
            lines: List of CSV lines
            delimiter: Delimiter character
            
        Returns:
            bool: True if first line appears to be a header
        """
        if len(lines) < 2:
            return False
        
        # Parse first two lines
        reader = csv.reader(lines[:2], delimiter=delimiter)
        rows = list(reader)
        
        if len(rows) < 2:
            return False
        
        first_row = rows[0]
        second_row = rows[1]
        
        # Check if first row contains expected column names
        first_row_lower = [col.lower().strip() for col in first_row]
        has_expected_columns = any(col in first_row_lower for col in self.EXPECTED_COLUMNS)
        
        if has_expected_columns:
            return True
        
        # Check if first row is all text and second row has similar structure
        # (heuristic: header is likely if first row is all non-numeric)
        try:
            # If we can convert most of second row to numbers, first row might be header
            numeric_count = sum(1 for val in second_row if val.strip() and val.replace('.', '').replace('-', '').isdigit())
            if numeric_count == 0 and len(first_row) == len(second_row):
                return True
        except:
            pass
        
        return False
    
    def _map_columns(self, header: List[str]) -> dict:
        """Map CSV columns to expected vocabulary fields.
        
        Args:
            header: List of column names from CSV
            
        Returns:
            dict: Mapping of CSV column index to field name
        """
        column_mapping = {}
        header_lower = [col.lower().strip() for col in header]
        
        for idx, col_name in enumerate(header_lower):
            if col_name in self.EXPECTED_COLUMNS:
                column_mapping[idx] = col_name
        
        return column_mapping
    
    def _parse_row(self, row: List[str], column_mapping: dict, has_header: bool, row_num: int) -> Tuple[Optional[dict], List[str]]:
        """Parse a single CSV row into a vocabulary entry dictionary.
        
        Args:
            row: List of values from CSV row
            column_mapping: Mapping of column indices to field names
            has_header: Whether CSV has a header row
            row_num: Line number in the original file (for error reporting)
            
        Returns:
            Tuple of (entry dict or None, list of error messages)
        """
        errors = []
        
        if not row or all(not val.strip() for val in row):
            return None, [f"Line {row_num}: Empty row"]
        
        entry = {}
        expected_col_count = len(column_mapping) if column_mapping else len(self.EXPECTED_COLUMNS)
        
        # Check for inconsistent column count
        if len(row) < expected_col_count:
            errors.append(f"Line {row_num}: Expected {expected_col_count} columns but found {len(row)}")
        elif len(row) > expected_col_count:
            errors.append(f"Line {row_num}: Expected {expected_col_count} columns but found {len(row)} (extra columns will be ignored)")
        
        if has_header and column_mapping:
            # Use column mapping from header
            for idx, field_name in column_mapping.items():
                if idx < len(row):
                    value = row[idx].strip()
                    entry[field_name] = value if value else None
                else:
                    entry[field_name] = None
                    if field_name in self.REQUIRED_COLUMNS:
                        errors.append(f"Line {row_num}: Missing required column '{field_name}'")
        else:
            # Use default column order: word, meaning, synonym, pronunciation, example
            for idx, field_name in enumerate(self.EXPECTED_COLUMNS):
                if idx < len(row):
                    value = row[idx].strip()
                    entry[field_name] = value if value else None
                else:
                    entry[field_name] = None
        
        # Validate required fields are present and non-empty
        if 'word' not in entry or not entry['word']:
            errors.append(f"Line {row_num}: Missing or empty required field 'word'")
            return None, errors
        if 'meaning' not in entry or not entry['meaning']:
            errors.append(f"Line {row_num}: Missing or empty required field 'meaning'")
            return None, errors
        
        # Validate field lengths
        if len(entry['word']) > 100:
            errors.append(f"Line {row_num}: Word '{entry['word'][:20]}...' exceeds maximum length of 100 characters")
            return None, errors
        
        return entry, errors
    
    def parse_csv(self, file_content: bytes, encoding: Optional[str] = None) -> ParseResult:
        """Parse CSV file content into vocabulary entries.
        
        Main parsing method that:
        1. Detects encoding if not provided
        2. Detects delimiter
        3. Detects header row
        4. Parses all rows into vocabulary entries
        5. Collects errors and warnings
        
        Args:
            file_content: Raw bytes of the CSV file
            encoding: Optional encoding (will be auto-detected if not provided)
            
        Returns:
            ParseResult: Object containing parsed entries, errors, and statistics
            
        Raises:
            CSVParseError: If file is malformed or unreadable
        """
        errors = []
        warnings = []
        entries = []
        
        # Detect encoding if not provided
        if encoding is None:
            try:
                encoding = self.detect_encoding(file_content)
            except CSVParseError as e:
                raise CSVParseError(f"Encoding detection failed: {str(e)}")
        
        # Decode file content
        try:
            text_content = file_content.decode(encoding)
        except UnicodeDecodeError as e:
            raise CSVParseError(
                f"Failed to decode file with encoding '{encoding}'. "
                f"The file may be corrupted or use a different encoding. "
                f"Error at byte position {e.start}: {str(e)}"
            )
        except LookupError as e:
            raise CSVParseError(f"Unknown encoding '{encoding}': {str(e)}")
        
        # Remove BOM if present
        if text_content.startswith('\ufeff'):
            text_content = text_content[1:]
        
        if not text_content.strip():
            raise CSVParseError("File is empty or contains only whitespace")
        
        # Detect delimiter
        try:
            delimiter = self.detect_delimiter(text_content)
        except CSVParseError as e:
            raise CSVParseError(f"Delimiter detection failed: {str(e)}")
        
        # Split into lines
        lines = text_content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            raise CSVParseError("File contains no data rows")
        
        # Detect header
        has_header = self._detect_header(non_empty_lines, delimiter)
        
        # Parse CSV
        try:
            reader = csv.reader(io.StringIO(text_content), delimiter=delimiter)
            rows = list(reader)
        except csv.Error as e:
            raise CSVParseError(
                f"CSV parsing failed: {str(e)}. "
                f"The file may be malformed or use an unsupported format."
            )
        except Exception as e:
            raise CSVParseError(f"Unexpected error while parsing CSV: {str(e)}")
        
        # Remove empty rows
        rows = [row for row in rows if row and any(cell.strip() for cell in row)]
        
        if not rows:
            raise CSVParseError("File contains no valid data rows")
        
        # Get column mapping if header exists
        column_mapping = {}
        start_row = 0
        
        if has_header:
            header = rows[0]
            column_mapping = self._map_columns(header)
            start_row = 1
            
            # Check if required columns are present
            mapped_fields = set(column_mapping.values())
            missing_required = [col for col in self.REQUIRED_COLUMNS if col not in mapped_fields]
            
            if missing_required:
                errors.append(f"Line 1 (header): Missing required columns: {', '.join(missing_required)}. Will attempt to use default column order.")
                warnings.append(f"Header detected but missing required columns: {', '.join(missing_required)}. Using default column order.")
                column_mapping = {}
                has_header = False
                start_row = 0
            else:
                # Check for unexpected columns
                expected_set = set(self.EXPECTED_COLUMNS)
                extra_cols = [col for col in mapped_fields if col not in expected_set]
                if extra_cols:
                    warnings.append(f"Line 1 (header): Unexpected columns found and will be ignored: {', '.join(extra_cols)}")
        
        # Parse data rows
        total_rows = len(rows) - start_row
        
        if total_rows == 0:
            raise CSVParseError("File contains no valid data rows after header")
        
        for row_idx, row in enumerate(rows[start_row:], start=start_row + 1):
            try:
                entry, row_errors = self._parse_row(row, column_mapping, has_header, row_idx)
                
                # Collect any errors from this row
                errors.extend(row_errors)
                
                if entry:
                    entries.append(entry)
            except Exception as e:
                errors.append(f"Line {row_idx}: Unexpected error - {str(e)}")
        
        # Handle duplicates before calculating success metrics
        if entries:
            entries, duplicate_warnings = self._handle_duplicates(entries)
            warnings.extend(duplicate_warnings)
        
        successful_rows = len(entries)
        
        # Add summary warnings
        if successful_rows < total_rows:
            warnings.append(f"Parsed {successful_rows} out of {total_rows} rows successfully")
        
        # Add informational message about what was detected
        if has_header:
            warnings.append(f"Detected header row with delimiter '{delimiter}' and encoding '{encoding}'")
        else:
            warnings.append(f"No header detected, using default column order with delimiter '{delimiter}' and encoding '{encoding}'")
        
        # If there are many errors, provide a summary
        if len(errors) > 10:
            error_summary = self._summarize_errors(errors)
            warnings.append(f"Error summary: {error_summary}")
        
        return ParseResult(
            entries=entries,
            errors=errors,
            warnings=warnings,
            total_rows=total_rows,
            successful_rows=successful_rows
        )
    
    def _handle_duplicates(self, entries: List[dict]) -> Tuple[List[dict], List[str]]:
        """Handle duplicate words in the parsed entries.
        
        Strategy: Merge duplicate entries by keeping the first occurrence and
        merging non-empty fields from subsequent occurrences. This ensures
        no data loss while maintaining a single entry per word.
        
        Args:
            entries: List of parsed vocabulary entry dictionaries
            
        Returns:
            Tuple of (deduplicated entries list, list of warning messages)
        """
        warnings = []
        seen_words = {}
        deduplicated = []
        
        for entry in entries:
            word = entry['word'].lower()  # Case-insensitive comparison
            
            if word not in seen_words:
                # First occurrence - add to results
                seen_words[word] = len(deduplicated)
                deduplicated.append(entry)
            else:
                # Duplicate found - merge with existing entry
                existing_idx = seen_words[word]
                existing_entry = deduplicated[existing_idx]
                
                # Track which fields were merged
                merged_fields = []
                
                # Merge non-empty fields from duplicate into existing entry
                for field in ['meaning', 'synonym', 'pronunciation', 'example']:
                    # If existing field is empty but duplicate has value, use duplicate's value
                    if not existing_entry.get(field) and entry.get(field):
                        existing_entry[field] = entry[field]
                        merged_fields.append(field)
                    # If both have values and they differ, append to existing (for meaning and example)
                    elif existing_entry.get(field) and entry.get(field) and existing_entry[field] != entry[field]:
                        if field in ['meaning', 'example']:
                            # Append additional meaning/example with separator
                            existing_entry[field] = f"{existing_entry[field]}; {entry[field]}"
                            merged_fields.append(field)
                
                # Create warning message
                if merged_fields:
                    warnings.append(
                        f"Duplicate word '{entry['word']}' found and merged. "
                        f"Fields merged: {', '.join(merged_fields)}"
                    )
                else:
                    warnings.append(
                        f"Duplicate word '{entry['word']}' found with identical data. "
                        f"Keeping first occurrence."
                    )
        
        # Add summary if duplicates were found
        duplicate_count = len(entries) - len(deduplicated)
        if duplicate_count > 0:
            warnings.insert(0, f"Found {duplicate_count} duplicate word(s) in CSV. Entries have been merged.")
        
        return deduplicated, warnings
    
    def _summarize_errors(self, errors: List[str]) -> str:
        """Create a summary of errors for better user feedback.
        
        Args:
            errors: List of error messages
            
        Returns:
            str: Summary of error types and counts
        """
        error_types = {
            'missing_required': 0,
            'column_count': 0,
            'field_length': 0,
            'other': 0
        }
        
        for error in errors:
            if 'Missing or empty required field' in error or 'Missing required column' in error:
                error_types['missing_required'] += 1
            elif 'Expected' in error and 'columns' in error:
                error_types['column_count'] += 1
            elif 'exceeds maximum length' in error:
                error_types['field_length'] += 1
            else:
                error_types['other'] += 1
        
        summary_parts = []
        if error_types['missing_required'] > 0:
            summary_parts.append(f"{error_types['missing_required']} missing required fields")
        if error_types['column_count'] > 0:
            summary_parts.append(f"{error_types['column_count']} column count mismatches")
        if error_types['field_length'] > 0:
            summary_parts.append(f"{error_types['field_length']} field length violations")
        if error_types['other'] > 0:
            summary_parts.append(f"{error_types['other']} other errors")
        
        return ", ".join(summary_parts) if summary_parts else "No errors"
