import os
import google.generativeai as genai
import fitz  # PyMuPDF for PDFs
import docx
from flask import Flask, request, render_template, jsonify
